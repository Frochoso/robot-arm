
from screen import Screen
from udp_config import Socket
import camera

sock=Socket()

disp = Screen()
disp.init_screen()
WIDTH = disp.get_screen_width()
HEIGHT = disp.get_screen_height()

print("Initializing system... Waiting to detect camera and body.")

while True:
    
    detection= camera.arm_detection(WIDTH, HEIGHT)
    
    message = detection[0]
    frame_rgb = detection[1]
    print(f"Message:{message}")
    sock.send_message(message.encode())

    if frame_rgb is not None:
        disp.display_image(frame_rgb)