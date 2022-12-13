import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
###############################

# GPIO 6 // Sarga Ledek // Barna hosszu
# GPIO 5 // Zold Ledek // Lila hosszu
# GPIO 16 // Piros Led // Szurke hosszu

while True:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.OUT)
    GPIO.output(5, True)
    time.sleep(1)
    GPIO.output(5, False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(6, GPIO.OUT)
    GPIO.output(6, True)
    time.sleep(1)
    GPIO.output(6, False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(16, True)
    time.sleep(1)
    GPIO.output(16, False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.OUT)
    GPIO.output(22, True)
    time.sleep(1)
    GPIO.output(22, False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, True)
    time.sleep(1)
    GPIO.output(27, False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.output(26, True)
    time.sleep(1)
    GPIO.output(26, False)
