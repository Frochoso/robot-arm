🤖 Gesture-Controlled Robotic Arm (MediaPipe + ESP32)
This project allows for real-time control of a robotic arm (or a motorized desk lamp) using a webcam and computer vision. The system tracks the user's arm movements, calculates the specific angles, and sends them wirelessly to a microcontroller that drives the physical servomotors, replicating the movement with almost zero latency.

🚀 Project Architecture
The project is divided into two main components that communicate over a local WiFi network using UDP packets:

The "Brain" (PC / Raspberry Pi):

Scans the human body using a webcam and MediaPipe.

Calculates the kinematics (forearm and hand inclination).

Applies an exponential smoothing filter to prevent jittering.

Displays the camera feed on a small TFT screen (ST7735) via SPI.

Sends the calculated target angles to the ESP32 via UDP.

The "Muscle" (ESP32):

Constantly listens for the target angles via UDP.

Controls the servomotors through a PCA9685 driver module (I2C).

Displays its assigned IP address and current motor status on an OLED screen (SSD1306) via I2C.

🛠️ Hardware Requirements
Webcam (USB or Raspberry Pi camera module).

PC or Raspberry Pi.

ESP32 Development Board.

PCA9685 Servo Driver Module.

Servomotors (x2).

ST7735 TFT Screen (SPI) for the main vision module.

SSD1306 OLED Screen (I2C) for the ESP32.

Independent power supply for the servos (⚠️ Important: Do not power the servos directly from the ESP32's 5V pin!).

💻 Software Requirements & Libraries
For Python (PC/Raspberry Pi)
Requires Python 3.10 or higher. Install the necessary dependencies by running:

Bash
pip install opencv-python mediapipe python-dotenv Pillow st7735
For the ESP32 (Arduino IDE)
Make sure you have the following libraries installed via the Arduino Library Manager:

Adafruit_PWMServoDriver

Adafruit_GFX

Adafruit_SSD1306

⚙️ Setup and Installation
1. Environment Variables (Python)
Create a file named .env in the root of your Python project to store the ESP32 network configuration:

Fragmento de código
ESP32_IP=192.168.X.X  # Replace with the actual IP shown on the ESP32's OLED screen
ESP32_PORT=4210
2. Python File Structure
Ensure your modules are structured as follows:

main.py: The main execution loop.

camera.py: Handles computer vision logic and angle calculations.

screen.py: Class to control the ST7735 TFT screen.

udp_config.py: Class for socket management and environment variables.

3. Uploading Code to the ESP32
Open the .ino file in the Arduino IDE.

Update your WiFi network credentials in the code:

C++
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
Upload the code to your ESP32 board.

Upon booting, the ESP32's OLED screen will display its local IP address. Copy this IP and paste it into your .env file.

▶️ Execution
Power up the ESP32 and wait for the OLED screen to confirm the WiFi connection and display the IP.

Run the main script on your computer or Raspberry Pi:

Bash
python main.py
Stand in front of the camera. The robot will start imitating your arm movements!

🧠 Smoothing Logic (Anti-Jitter)
Because AI pose estimation can have slight variations between frames, this project implements a mathematical filter (Exponential Smoothing) inside camera.py. This feature absorbs micro-vibrations, ensuring that the physical motors move smoothly and preventing hardware damage over time.