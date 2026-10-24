import RPi.GPIO as GPIO
from picamera2 import Picamera2, Preview
import time
import requests

#picam2 = Picamera2()
#config = picam2.create_preview_configuration()

num = 1

tumblrBool = False

LED_PIN = 11

def button_callback(channel):
	global num
	message = f"Picture taken and saved as pic{num}.jpg in Pictures folder"
	file = f"/home/camera/Pictures/pic{num}.jpg"
	picam2 = Picamera2()
	config = picam2.create_preview_configuration()
	picam2.configure(config)
	picam2.start_preview(Preview.DRM)
	picam2.start()
	time.sleep(2)
	picam2.capture_file(file)
	picam2.close()
	print(message)
	num = num + 1

def is_tumblr_up():
	url = "https://www.tumblr.com"
	timeout = 10
	global tumblrBool
	r = requests.get(url, timeout=timeout)
	if r.status_code == requests.codes.ok:
		tumblrBool = True
		print("yep, tumblr's up")
		GPIO.output(LED_PIN, GPIO.HIGH)
	else:
		tumblrBool = False
		print("nope, no connection")
		GPIO.output(LED_PIN, GPIO.LOW)

GPIO.setwarnings(False) #ignore warnings
GPIO.setmode(GPIO.BOARD) #use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #set pin 10 as input and set initial value to be pulled low (off)

GPIO.setup(LED_PIN, GPIO.OUT)

GPIO.add_event_detect(10, GPIO.RISING, callback=button_callback) #set up event on pin 10 rising edge

while True:
	is_tumblr_up()
	time.sleep(30)

message = input("Press enter to quit\n\n") #run until someone presses enter

GPIO.cleanup() #cleanup
