# Rideau Canal Sensor Simulation

## Overview
This repository hosts the Python-based simulator for the Rideau Canal Ice Monitoring Project. It mimics the behavior of physical IoT devices sending real-time environmental telemetry.

* **What the simulator does:** Generates semi-random, location-based readings for ice thickness and temperature. It runs continuously, sending data packets to the cloud every few seconds.
* **Technologies used:** **Python 3.x**, **Azure IoT SDK for Python** (`azure-iot-device`).

---

## Prerequisites
* Python 3.x installed.
* A registered device in Azure IoT Hub (requires the **Device Connection String**).

---

## Installation
1.  Clone this repository.
2.  Install dependencies using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```
---

## Configuration
1.  Create a file named **`.env`** in the root directory.
2.  Paste the format from `.env.example` and replace the placeholder with your actual **IoT Hub Device Connection String**.

---

## Usage
To start the simulation, execute the main script:
```bash
python sensor_simulator.py
```
---

## Code Structure
* sensor_simulator.py: Main application file containing the device client setup, data generation logic, and the loop for sending messages.
* requirements.txt: Lists necessary Python packages (azure-iot-device, python-dotenv).
* run_telemetry_client(): Initializes the IoT Hub client and connects securely using the connection string.
* generate_telemetry(): Creates a JSON payload with current timestamp, location, and randomized environmental readings.

---

## Sensor Data Format
The simulator sends data in a JSON payload to the IoT Hub.

### JSON Schema

* IceThickness_cm: Simulated ice thickness in centimeters.
* SurfaceTemp_C: Simulated surface temperature in Celsius.
* timestamp: UTC timestamp of the measurement.
* location: The name of the simulated device/location (dows-lake, etc.).

### Example Output
```
{
  "IceThickness_cm": 27.5,
  "SurfaceTemp_C": -8.1,
  "timestamp": "2025-12-03T01:00:00.000Z",
  "location": "fifth-avenue"
}
```

---

## Troubleshooting

* Error: ModuleNotFoundError: Run pip install -r requirements.txt.
* Error: UnauthorizedError: Check your .env file; the Device Connection String is incorrect or expired.
* Data not arriving at IoT Hub: Verify the device status is Enabled in the Azure Portal.









