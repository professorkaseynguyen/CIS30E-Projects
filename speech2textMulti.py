import speech_recognition as sr
from gpiozero import LED, Button
import RPi.GPIO as GPIO
from time import sleep
import timeit
from multiprocessing import Process
import sys

led = LED(22)   #Can be replaced or added with other output devices
button = Button(25)

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)


def translate():
    global starttime
    starttime = timeit.default_timer()
    stated = r.recognize_google(audio)
    stated = stated.lower()
    print("You said:" + stated)
    p = Process(target=action, args=(stated,))
    p.start()
    p.join()
    
                 
def action(stated):
    if stated == passkey:
        print("LOCK DISENGAGED")
        GPIO.output(23, 1)
        led.on()
        print("Time to execute: ", timeit.default_timer()-starttime)
        sleep(5)            #Wait for seconds to relock 
        led.off()
        GPIO.output(23, 0)
        print("LOCK ENGAGED")
        print("After 5 second wait: ", timeit.default_timer()-starttime)
                
    if stated == "quit":
        print("Time to quit: ", timeit.default_timer()-starttime)
        quit()

passkey = "password"
r = sr.Recognizer()

while True:
    while(button.is_pressed):   #To reduce amount of active listening time
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("What is the password:")
            audio = r.listen(source, phrase_time_limit=5)

        try:
            translate()
                 
        except sr.UnknownValueError:
            print("Failed")

        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition")
