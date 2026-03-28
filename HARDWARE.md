# Hardware Setup & Wiring Guide

This document explains how to wire the physical components of the Gesture-Controlled Robotic Arm.

## ⚠️ CRITICAL WARNING
**Never power the servomotors directly from the ESP32 or Raspberry Pi 5V/3.3V pins.** Servos draw high current spikes that will instantly fry your microcontrollers. Always use an external 5V power supply (like a battery pack or a dedicated 5V/2A+ wall adapter) connected to the PCA9685 power terminal.

---

## 1. The Muscle: ESP32 Wiring

The ESP32 acts as the receiver. It communicates with the servo driver and the OLED screen using the **I2C protocol** (which allows multiple devices to share the same pins).

### Components Required
* ESP32 Development Board
* PCA9685 16-Channel PWM Servo Driver
* SSD1306 128x64 OLED Screen (I2C)
* 2x Servomotors (Forearm and Hand)
* External 5V Power Supply

### I2C Shared Bus Connections
Both the PCA9685 and the SSD1306 OLED screen connect to the same I2C pins on the ESP32.

| ESP32 Pin | PCA9685 Pin | SSD1306 OLED Pin | Description |
| :--- | :--- | :--- | :--- |
| **3.3V** | VCC | VDD / VCC | Logic power (Do NOT use for servos) |
| **GND** | GND | GND | Common Ground |
| **GPIO 21** | SDA | SDA | I2C Data Line |
| **GPIO 22** | SCL | SCK / SCL | I2C Clock Line |

### Servo Connections (To PCA9685)
* **Forearm Servo:** Plug into **Channel 0** on the PCA9685.
* **Hand Servo:** Plug into **Channel 1** on the PCA9685.
* **External Power:** Connect your external 5V power supply to the **V+ and GND screw terminal** block on the PCA9685. Ensure the ground of the external supply shares a connection with the ESP32 ground.

---

## 2. The Brain: Host / Raspberry Pi Wiring

If you are running the Python code on a Raspberry Pi, it drives a small TFT screen via the **SPI protocol** to show the camera feed. 

*(Note: If you are running the Python code on a standard PC/Laptop, you can bypass the ST7735 screen logic or use standard OpenCV `cv2.imshow()` windows instead).*

### Components Required
* Raspberry Pi (3/4/5)
* ST7735 128x160 TFT Screen (SPI)

### SPI Connections
Based on the Python code configuration (`port=0, cs=0, dc=25, rst=24`), wire the ST7735 screen to the Raspberry Pi GPIO header as follows:

| ST7735 Pin | Raspberry Pi Pin (BCM) | Description |
| :--- | :--- | :--- |
| **VCC** | 3.3V (Pin 1 or 17) | Power |
| **GND** | GND (Pin 6, 9, 14, etc.) | Ground |
| **SDA / MOSI** | GPIO 10 (Pin 19) | SPI Data (MOSI) |
| **SCL / SCLK** | GPIO 11 (Pin 23) | SPI Clock |
| **CS / CE** | GPIO 8 (Pin 24) | SPI Chip Select (`cs=0`) |
| **DC / A0** | GPIO 25 (Pin 22) | Data / Command (`dc=25`) |
| **RST / RES** | GPIO 24 (Pin 18) | Reset (`rst=24`) |
| **BLK / LED** | 3.3V (Optional) | Backlight (Always on) |

### Troubleshooting
* **ESP32 keeps restarting:** The servos are likely drawing too much power. Double-check that your external power supply is securely connected to the PCA9685 block and that its ground is tied to the ESP32's ground.
* **TFT Screen stays white (Raspberry Pi):** Ensure SPI is enabled in the Raspberry Pi configuration (`sudo raspi-config` > Interface Options > SPI > Enable).