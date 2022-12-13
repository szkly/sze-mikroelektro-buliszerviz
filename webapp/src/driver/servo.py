import logging
from time import sleep
import RPi.GPIO as GPIO


class Servo:
    def __init__(self, pin):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initializing servo on pin {pin}...")
        self.pin = pin

        GPIO.setup(pin, GPIO.OUT)
        self.servo = GPIO.PWM(self.pin, 50)
        self.servo.start(0)

        self.logger.info(f"Successfully initialized servo on pin {pin}!")

    def turn(self, angle):
        self.servo.ChangeDutyCycle(2 + (angle / 18))
        sleep(0.5)
        self.servo.ChangeDutyCycle(0)

    def __del__(self):
        self.logger.info(f"Turning off servo on pin {self.pin}...")

        self.servo.stop()

        self.logger.info(f"Successfully turned off servo on pin {self.pin}!")
