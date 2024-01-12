import RPi.GPIO as GPIO
import os

# GPIO pin for the LED
led = 13

# Set up GPIO mode and initial state
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
pwm = GPIO.PWM(led, 1)  #set up pwm with frequency 1 Hz

while True:
  # get status of service
  serviceStatus = os.system('systemctl is-active --quiet speaker-agent.service')
  # if service is inactive start led blinking
  if serviceStatus != 0:
    pwm.start(50)
