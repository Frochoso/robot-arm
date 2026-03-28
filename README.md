# Gesture-Controlled Robotic Arm

## Overview
This repository contains a full-stack robotic arm control system that bridges computer vision with embedded hardware. The project provides an intuitive, gesture-based interface for controlling a physical robotic arm (or motorized lamp) in real-time. 

By utilizing a webcam, the system tracks the user's arm movements, calculates the corresponding kinematics, applies mathematical smoothing to prevent erratic behavior, and wirelessly transmits these coordinates to an ESP32 microcontroller. The ESP32 then drives physical servomotors to mirror the user's exact arm posture with minimal latency.

## Architecture
The project is divided into two distinct ecosystems:
1. **The Brain (Python / Raspberry Pi):** Runs on a Raspberry Pi. It uses **OpenCV** to capture video and **MediaPipe** to detect the human pose. It calculates the angles of the forearm and hand, filters the data using an exponential smoothing algorithm, displays the feed on a local TFT screen (ST7735), and sends the target angles via UDP sockets.
2. **The Muscle (C++ / ESP32):** Acts as the receiver. It connects to the local WiFi, listens for UDP packets containing target angles, and commands the servomotors via a **PCA9685** PWM driver over I2C. It also outputs its network status and current servo angles to an OLED screen (SSD1306).

## Features
- **Real-Time Pose Tracking:** Utilizes MediaPipe's lightweight pose model for fast, accurate detection of the elbow, wrist, and index finger.
- **Wireless Telemetry:** Uses low-latency UDP packets to send formatted string commands (e.g., `F90H45`) across the local WiFi network.
- **Hardware Integration:** - Drives multiple servos smoothly using the PCA9685 16-channel PWM controller.
  - Provides visual system feedback via an I2C OLED display (ESP32 side) and an SPI TFT display (Python side).
- **Anti-Jitter Smoothing:** Incorporates a custom exponential smoothing filter (`alpha = 0.2`) to absorb AI estimation micro-vibrations, protecting the physical servos from damage.
- **Modular Design:** Object-oriented Python architecture separates camera logic, screen rendering, and network configuration for easy maintenance.

## Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/Frochoso/robot-arm.git](https://github.com/Frochoso/robot-arm.git)
   ```
2. Navigate to the project directory:
   ```bash
   cd gesture_recognition
   ```
3. Initialize the environment:
   ```bash
   poetry env use 3.10
   poetry env activate
   ```
4. Install required dependencies:
   ```bash
   poetry install
   ```
5. **Environment Configuration:**
   Create a `.env` file in the root directory containing your ESP32 network credentials. (You can find the IP on the ESP32's OLED screen once it boots).
   ```env
   ESP32_IP=192.168.X.X
   ESP32_PORT=4210
   ```

## Usage
1. Power on the ESP32 and the external power supply for the servos.
2. Wait for the ESP32 OLED screen to display "CONNECTED!" and its assigned IP.
3. To execute the tracking program, run:
   ```bash
   poetry run python3 main.py
   ```
4. Step in front of the camera. Ensure your right arm is visible, and the robotic arm will begin mirroring your movements.

## Acknowledgments
- Thanks to Nujabes and all my friends who supported me along the way.
``` 
C'est la vie,
as they say L-O-V-E eloquently, see every dream has a part two.
Never same, you got to keep it tight,
always just like back then, now hear me out.
```