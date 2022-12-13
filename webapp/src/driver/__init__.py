import logging
import multiprocessing
from time import sleep

from playsound import playsound

from . import led, utils
from .display import Display
from .pins import SERVO_PIN, DoorLight, PartyLight
from .servo import Servo


class Driver():
    def __init__(self, url, song_file_path):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing GPIO interface...")

        self.url = url
        self.song_file_path = song_file_path

        utils.init_gpio()

        pin_clusters_to_setup = [DoorLight, PartyLight]
        self.pins = utils.setup_pins(pin_clusters_to_setup)

        self.servo_motor = Servo(pin=SERVO_PIN)
        self.door_display = Display(width=128, height=32, url=url)

        self.idle()
        self.run()

        self.logger.info("Successfully initialized GPIO interface!")

    def run(self):
        self.idle_party_thread = multiprocessing.Process(name="idle_party",
                                                         target=self.idle_party, daemon=True)

        self.idle_party_thread.start()

    def idle(self):
        led.on(DoorLight.RED)
        self.door_display.idle()

    def idle_party(self):
        # setting the block variable to false enables background execution (i.e. the song continues in the background)
        playsound(self.song_file_path, block=False)

        RHYTHM = 0.48665 / 2
        while True:
            led.blink(PartyLight.RED, timing=RHYTHM)
            led.blink(PartyLight.GREEN, timing=RHYTHM)
            led.blink(PartyLight.AMBER, timing=RHYTHM)

    def on_approval(self):
        led.off(DoorLight.RED)
        led.on(DoorLight.AMBER)

        self.door_display.show_loading_sequence()

        led.blink(DoorLight.AMBER, 4)

        self.handle_opening()
        self.handle_closing()

    def handle_opening(self):
        self.logger.info("Opening door...")

        self.door_display.clear()
        self.door_display.show_message("Ajto nyitasa", 0, 0,
                                       should_center_horizontally=True)
        self.door_display.show_message("Jo szorakozast!", 0,
                                       16, should_center_horizontally=True)

        led.off(DoorLight.AMBER)
        led.on(DoorLight.GREEN)

        sleep(1)

        self.servo_motor.turn(angle=0)

        self.logger.info("Door is open!")
        sleep(3)

    def handle_closing(self):
        self.logger.info("Closing door...")

        self.door_display.clear()
        self.door_display.show_message(
            "Vigyazat!", 0, 0, should_center_horizontally=True)
        self.door_display.show_message("Ajto csukasa", 0,
                                       16, should_center_horizontally=True)

        led.off(DoorLight.GREEN)
        led.blink(DoorLight.AMBER, 4)

        led.off(DoorLight.AMBER)
        led.on(DoorLight.RED)

        sleep(1)

        self.servo_motor.turn(angle=155)
        led.off(DoorLight.RED)

        self.logger.info("Door is closed!")

    def on_denial(self):
        self.logger.info("Door is staying shut")

        self.door_display.clear()
        self.door_display.show_message(
            "Belepes megtagadva", 0, 0, should_center_horizontally=True)
        self.door_display.show_message(
            "Csao!", 0, 16, should_center_horizontally=True)

        led.blink(DoorLight.RED, 4)

        sleep(1)

    def __del__(self):
        logging.info("Deleting an instance of the Driver class...")

        self.idle_party_thread.terminate()

        utils.clean_up_pins(self.pins)

        logging.info("Successfully deleted an instance of the Driver class!")
