from PIL import Image
import st7735

class Screen:
    def __init__(self):
        self.disp = st7735.ST7735(port=0, cs=0, dc=25, backlight=None, rst=24, width=128, 
                        height=160, rotation=0, spi_speed_hz=10000000, offset_left=0, offset_top=0)

    def init_screen(self):
        self.disp.begin()
        
    def get_screen_width(self):
        return self.disp.width

    def get_screen_height(self):
        return self.disp.height

    def display_image(self, frame_rgb):
        img_pil = Image.fromarray(frame_rgb, mode='RGB')
        self.disp.display(img_pil)