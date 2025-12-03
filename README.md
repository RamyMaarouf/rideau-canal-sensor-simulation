# Rideau Canal Sensor Simulation

## Overview
This repository hosts the Python-based simulator for the Rideau Canal Ice Monitoring Project. It mimics the behavior of physical IoT devices sending real-time environmental telemetry.

* **What the simulator does:** Generates semi-random, location-based readings for ice thickness and temperature. It runs continuously, sending data packets to the cloud every few seconds.
* **Technologies used:** **Python 3.x**, **Azure IoT SDK for Python** (`azure-iot-device`).

---

## Prerequisites
* Python 3.x installed.
* A registered device in Azure IoT Hub (requires the **Device Connection String**).

### Installation
1.  Clone this repository.
2.  Install dependencies using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration
1.  Create a file named **`.env`** in the root directory.
2.  Paste the format from `.env.example` and replace the placeholder with your actual **IoT Hub Device Connection String**.

## Usage
To start the simulation, execute the main script:
```bash
python sensor_simulator.py
