# 🧊 Rideau Canal Sensor Simulation

This repository contains the Python script used to simulate IoT devices sending environmental data (Ice Thickness and Surface Temperature) to Azure IoT Hub.

## Prerequisites

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Setup and Usage

1.  **Get Connection String:** Register a device in your Azure IoT Hub (e.g., `dows-lake`) and copy its **Device Connection String**.
2.  **Configure .env:** Create a file named `.env` in this directory and paste your connection string, referencing the format in `.env.example`.
3.  **Run the Script:** Execute the main simulation script. It will run indefinitely, sending data every few seconds.

    ```bash
    python sensor_simulator.py
    ```

## How it Works

The script reads the device connection string from the `.env` file and uses the `azure-iot-device` SDK to connect and send JSON messages to the cloud.
