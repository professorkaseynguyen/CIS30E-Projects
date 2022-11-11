import speech_recognition as sr
from gpiozero import LED, Button
import RPi.GPIO as GPIO
from time import sleep


led = LED(22)   #Can be replaced or added with other output devices
button = Button(25)

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)

passkey = "password"
r = sr.Recognizer()

while True:
    while(button.is_pressed):   #To reduce amount of active listening time
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("What is the password:")
            audio = r.listen(source, phrase_time_limit=5)

        try:
            stated = r.recognize_google(audio)
            stated = stated.lower()
            print("You said:" + stated)
            if stated == passkey:
                print("HAACHAMA CHAMAAA")
                GPIO.output(23, 1)
                led.on()
                sleep(5)
                led.off()
                GPIO.output(23, 0)
                
            if stated == "quit":
                quit()
        
        except sr.UnknownValueError:
            print("Failed")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition")

