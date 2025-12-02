# sensor_simulator.py

import asyncio
import json
import random
import time
import os
from datetime import datetime, timezone
from azure.iot.device import IoTHubDeviceClient, Message

# --- Configuration (Replace with your actual Connection Strings) ---
# NOTE: In a real project, these would be loaded from a .env file for security.
DEVICE_CONNECTION_STRINGS = {
    "dows-lake": "HostName=your-iot-hub.azure-devices.net;DeviceId=dows-lake;SharedAccessKey=...",
    "fifth-avenue": "HostName=your-iot-hub.azure-devices.net;DeviceId=fifth-avenue;SharedAccessKey=...",
    "nac": "HostName=your-iot-hub.azure-devices.net;DeviceId=nac;SharedAccessKey=...",
}
SEND_FREQUENCY_SECONDS = 10

# --- Sensor Data Logic ---

# Realistic ranges for an open skateway.
# Ice Thickness (cm): Safe range is > 25cm.
# Surface Temp (°C): Ideal for skating is -5C to -15C.
# Snow Accumulation (cm): Low to moderate.
SENSOR_RANGES = {
    "IceThickness": (28.0, 35.0), 
    "SurfaceTemperature": (-12.0, -2.0),
    "SnowAccumulation": (0.0, 5.0),
    "ExternalTemperature": (-15.0, -1.0)
}

def generate_telemetry(location: str) -> str:
    """Generates a JSON payload with sensor readings."""
    
    # Generate random readings within realistic bounds
    ice_thickness = round(random.uniform(*SENSOR_RANGES["IceThickness"]), 1)
    surface_temp = round(random.uniform(*SENSOR_RANGES["SurfaceTemperature"]), 1)
    snow_acc = round(random.uniform(*SENSOR_RANGES["SnowAccumulation"]), 1)
    external_temp = round(random.uniform(*SENSOR_RANGES["ExternalTemperature"]), 1)

    # Create the required JSON payload
    data = {
        "location": location,
        "IceThickness": ice_thickness,
        "SurfaceTemperature": surface_temp,
        "SnowAccumulation": snow_acc,
        "ExternalTemperature": external_temp,
        "Timestamp": datetime.now(timezone.utc).isoformat()  # ASA uses this for TUMBING WINDOW
    }
    return json.dumps(data)

async def send_telemetry(device_id: str, conn_str: str):
    """Initializes device client and starts the sending loop."""
    try:
        # Create IoTHubDeviceClient instance
        client = IoTHubDeviceClient.create_from_connection_string(conn_str)
        print(f"[{device_id}] Client connected.")
        
        await client.connect()

        while True:
            # Generate the data payload
            telemetry = generate_telemetry(device_id)
            
            # Create the message and send
            message = Message(telemetry)
            
            # Add custom property (optional, but good practice)
            message.custom_properties["sensorType"] = "RideauSkateway"
            
            await client.send_message(message)
            print(f"[{device_id}] Sent message: {telemetry}")
            
            # Wait for the next cycle
            await asyncio.sleep(SEND_FREQUENCY_SECONDS)

    except Exception as e:
        print(f"[{device_id}] ERROR: {e}")
        await client.shutdown()
        
    finally:
        print(f"[{device_id}] Client shutting down.")

def main():
    print("--- Starting Rideau Canal Sensor Simulation ---")
    
    # Create a list of concurrent tasks, one for each device
    tasks = []
    for device_id, conn_str in DEVICE_CONNECTION_STRINGS.items():
        if conn_str.startswith("HostName="): # Basic check to ensure credentials are set
            tasks.append(send_telemetry(device_id, conn_str))
        else:
            print(f"[CRITICAL] Connection string not set for {device_id}. Skipping.")

    if not tasks:
        print("No valid devices configured. Please check DEVICE_CONNECTION_STRINGS.")
        return

    # Run all tasks concurrently
    asyncio.run(asyncio.wait(tasks))

if __name__ == "__main__":
    main()
