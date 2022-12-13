import logging

import adafruit_ssd1306
import busio
from board import SCL, SDA
from PIL import Image, ImageDraw, ImageFont

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 32

DISPLAY_PADDING = -2
DISPLAY_TOP = DISPLAY_PADDING
DISPLAY_BOTTOM = DISPLAY_HEIGHT - DISPLAY_PADDING


class Display:
    def __init__(self, width, height, padding=-2, url="https://example.com"):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing an instance of the Display class...")

        self.width = width
        self.height = height

        self.padding = padding
        self.top = self.padding
        self.bottom = self.height - self.padding

        i2c = busio.I2C(SCL, SDA)
        self.module = adafruit_ssd1306.SSD1306_I2C(
            self.width, self.height, i2c)

        self.reset()

        self.image = Image.new('1', (self.width, self.height))

        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        self.font = ImageFont.load_default()

        self.url = url

        self.logger.info(
            "Successfully initialized an instance of the Display class!")

    def idle(self):
        self.clear()
        self.show_message("A party folyamatban", 0, 0,
                          should_center_horizontally=True)
        self.show_message(self.url, 0, 24)

    def show_message(self, message, x, y, should_center_horizontally=False):
        if should_center_horizontally:
            x += self.calculate_center(message)

        self.draw.text((x, self.top + y), message, font=self.font, fill=255)

        self.module.image(self.image)
        self.module.show()

    def calculate_center(self, message):
        absolute_center = self.width / 2

        # On average 1 letter is 5.75 pixels wide on the display
        FONT_WIDTH = 5.75
        center = int(absolute_center - ((len(message) * FONT_WIDTH) / 2))

        if (center < 0):
            return 0
        else:
            return center

    def show_loading_sequence(self, current_progress=0):
        self.clear()

        current_progress = current_progress if current_progress > 0 else int(
            self.width)

        self.show_message("Belepes engedelyezve", 0, 0,
                          should_center_horizontally=True)

        for i in range(0, current_progress, 4):
            self.draw_progress_bar(i)

        self.show_message("Jo szorakozast!", 0, 24,
                          should_center_horizontally=True)

    def draw_progress_bar(self, x, line_height=8):
        # 3 blocks (0 - 4)
        progress_bar_start = 0 + line_height
        progress_bar_end = 4 + line_height

        for i in range(progress_bar_start, progress_bar_end):
            self.show_message(".", x, i)

    def clear(self):
        self.logger.info("Clearing display...")

        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.module.show()

        self.logger.info("Successfully cleared display!")

    def reset(self):
        self.logger.info("Resetting display...")

        self.module.fill(0)
        self.module.show()

        self.logger.info("Successfully reset display!")

    def __del__(self):
        self.logger.info("Deleting an instance of the Display class...")

        self.clear()
        self.reset()

        self.logger.info(
            "Successfully deleted an instance of the Display class!")
