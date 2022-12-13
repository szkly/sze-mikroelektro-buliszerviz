import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
servo = GPIO.PWM(17, 50)
servo.start(0)

try:
    angle = float(0)
    print("Ajto nyitása")
    servo.ChangeDutyCycle(2+(angle/18))
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)

    time.sleep(3)

    angle = float(160)
    print("Ajto csukása")
    servo.ChangeDutyCycle(2+(angle/18))
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)

finally:
    servo.stop()
    GPIO.cleanup()
