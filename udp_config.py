import os
from dotenv import load_dotenv, find_dotenv
import socket

class Socket:
    
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        self.connection_info = self.get_connection()
        
    def get_connection(self): 
        try:
            env_path = find_dotenv(".env")
            if not env_path:
                raise FileNotFoundError(".env file not found.")

            load_dotenv(env_path)

            esp32_ip = os.getenv("ESP32_IP")
            esp32_port = os.getenv("ESP32_PORT")

            return {
                "IP": esp32_ip,
                "PORT": int(esp32_port) if esp32_port else 0
            }

        except Exception as e:
            print(f"Error loading .env file:  {e}")
            return {}

    def send_message(self, message):
      
        if "IP" in self.connection_info and "PORT" in self.connection_info:
            
            self.sock.sendto(message, (self.connection_info["IP"], self.connection_info["PORT"]))
        else:
            print("Error: Message couldn't be sent, please add the ESP32 IP and port inside the .env file")