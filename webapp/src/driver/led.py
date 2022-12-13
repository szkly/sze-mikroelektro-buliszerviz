import RPi.GPIO as GPIO
from time import sleep


def on(pin):
    GPIO.output(pin.value, True)


def off(pin):
    GPIO.output(pin.value, False)


BLINK_TIMING = 0.2


def blink(pin, count=1, timing=BLINK_TIMING, party_mode=False):
    # the sequence goes like this: off - on - off
    BLINK_PIN_SEQUENCE = [False, True, False]
    BLINK_PIN_PARTY_SEQUENCE = [True, False]

    sequence = BLINK_PIN_PARTY_SEQUENCE if party_mode else BLINK_PIN_SEQUENCE

    i = 0
    while i < count:
        for state in sequence:
            GPIO.output(pin.value, state)
            sleep(timing)

        i += 1
