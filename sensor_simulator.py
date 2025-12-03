# sensor_simulator.py (FINAL CONSOLIDATED SCRIPT)

import asyncio
import json
import random
from datetime import datetime, timezone
from azure.iot.device import IoTHubDeviceClient, Message

# --- 🛑 Configuration (FINAL CONSOLIDATED SETUP) ---
# Using the latest confirmed keys from your input
DEVICE_CONFIGS = {
    "dows-lake": {
        "host_name": "RCSIoT.azure-devices.net",
        # Using the key ending in 4E= which was presented first, just in case 
        "device_id": "dows-lake",
        "key": "IBDD4jvsCvmgx6fxJje5w/0IxVk2NGkLp2b38H96/4E="
    }, 
    "fifth-avenue": {
        "host_name": "RCSIoT.azure-devices.net",
        "device_id": "fifth-avenue",
        "key": "LRHfkBm+xQ9uW7BjB/G0uBX1IjMFvSR03AIoTJJGeCM="
    }, 
    "nac": {
        "host_name": "RCSIoT.azure-devices.net",
        "device_id": "nac",
        "key": "oRYJvr1r5IOt0xUmDScKXz1pU9U5tbbhnAIoTJQtKYc="
    },
}
SEND_FREQUENCY_SECONDS = 10

# --- Sensor Data Logic ---

SENSOR_RANGES = {
    "IceThickness": (28.0, 35.0), 
    "SurfaceTemperature": (-12.0, -2.0),
    "SnowAccumulation": (0.0, 5.0),
    "ExternalTemperature": (-15.0, -1.0)
}

def generate_telemetry(location: str) -> str:
    """Generates a JSON payload with sensor readings."""
    
    ice_thickness = round(random.uniform(*SENSOR_RANGES["IceThickness"]), 1)
    surface_temp = round(random.uniform(*SENSOR_RANGES["SurfaceTemperature"]), 1)
    snow_acc = round(random.uniform(*SENSOR_RANGES["SnowAccumulation"]), 1)
    external_temp = round(random.uniform(*SENSOR_RANGES["ExternalTemperature"]), 1)

    data = {
        "location": location,
        "IceThickness": ice_thickness,
        "SurfaceTemperature": surface_temp,
        "SnowAccumulation": snow_acc,
        "ExternalTemperature": external_temp,
        "Timestamp": datetime.now(timezone.utc).isoformat()
    }
    return json.dumps(data)

# --- Updated send_telemetry function using components ---
async def send_telemetry(device_id: str, config: dict):
    """Initializes device client and starts the sending loop using components."""
    client = None
    try:
        # Use create_from_symmetric_key to connect using individual components
        client = IoTHubDeviceClient.create_from_symmetric_key(
            symmetric_key=config['key'],
            hostname=config['host_name'],
            device_id=config['device_id'],
        )
        print(f"[{device_id}] Client connected.")
        
        client.connect() 

        while True:
            telemetry = generate_telemetry(device_id)
            message = Message(telemetry)
            message.custom_properties["sensorType"] = "RideauSkateway"
            
            client.send_message(message)
            print(f"[{device_id}] Sent message: {telemetry}")
            
            await asyncio.sleep(SEND_FREQUENCY_SECONDS)

    except Exception as e:
        print(f"[{device_id}] ERROR: {e}")
        if client:
            await client.shutdown()
        
    finally:
        print(f"[{device_id}] Client shutting down.")


# --- Async Runner Function (Correct structure) ---

async def run_simulations():
    """Sets up the concurrent tasks and runs the event loop."""
    tasks = []
    
    # Iterate over the new DEVICE_CONFIGS dictionary
    for device_id, config in DEVICE_CONFIGS.items():
        # Pass the config dictionary to send_telemetry
        task = asyncio.create_task(send_telemetry(device_id, config)) 
        tasks.append(task)

    if not tasks:
        print("No valid devices configured. Please check DEVICE_CONFIGS.")
        return

    # Run all tasks concurrently and wait for them to complete
    await asyncio.gather(*tasks)


def main():
    print("--- Starting Rideau Canal Sensor Simulation ---")
    
    # Use asyncio.run() once as the entry point
    try:
        asyncio.run(run_simulations())
        
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()