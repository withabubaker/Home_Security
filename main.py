import RPi.GPIO as GPIO
import time
import boto3
motion_pin = 18
buzzer_pin = 17
# Create an SNS client
client = boto3.client(
    "sns",
    aws_access_key_id="AccessKeyHere",
    aws_secret_access_key="SecretAccessKeyHere",
    region_name="us-east-1"
)
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motion_pin, GPIO.IN)  # Read output from PIR motion sensor
    GPIO.setup(buzzer_pin, GPIO.OUT)  # Output to buzzer
def loop():
    while True:
        i = GPIO.input(motion_pin)
        if i == 0:  # When output from motion sensor is LOW
            print("No intruders", i)
            time.sleep(0.5)
        elif i == 1:  # When output from motion sensor is HIGH
            print("Intruder detected", i)
            GPIO.output(buzzer_pin, GPIO.HIGH)
            # Send your sms message.
            client.publish(
                PhoneNumber="PhoneNumberHere",
                Message="Intruder detected! Please check your camera!"
            )
            time.sleep(3)
           GPIO.output(buzzer_pin, GPIO.LOW)
if __name__ == '__main__':
    print('Program is starting')
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
