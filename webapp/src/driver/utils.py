import RPi.GPIO as GPIO


def init_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)


def setup_pins(pin_clusters):
    pins = get_pins(pin_clusters)
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)

    return pins


def get_pins(pin_clusters):
    pins_to_setup = [
        pin for pin_cluster in pin_clusters for pin in get_pin_values(pin_cluster)]

    return pins_to_setup


def get_pin_values(cluster):
    return [pin.value for pin in cluster]


def clean_up_pins(pins):
    for pin in pins:
        GPIO.output(pin, False)

    GPIO.cleanup()
