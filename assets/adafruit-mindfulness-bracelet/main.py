# Mindfulness Bracelet sketch for Adafruit Gemma.  Briefly runs
# vibrating motor (connected through transistor) at regular intervals.

import time
import board
from digitalio import DigitalInOut, Direction
from analogio import AnalogOut
from touchio import TouchIn
import adafruit_dotstar

debug = False

#turn off the dotstar
dotstar = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
dotstar.brightness = 0
dotstar.fill((0, 0, 255))

# vibrating disc mini motor disc connected on D2
#use as an analog out so can control how much the motor vibrates
vibrating_disc = AnalogOut(board.A0)
# quarter power: 16384
# half power: 32768
# full power: 65535
# NOTE: the vibration amount depends on voltage in. If powered by USB,
# quarter power is about right. If powered by a single 3V watch battery, 
# full power is the way to go
vibrating_disc_on_value = 65535


# Built in red LED
led = False
if debug:
    led = DigitalInOut(board.D13)
    led.direction = Direction.OUTPUT

# Capacitive touch on A2
touch2 = TouchIn(board.A2)

on_time = 1     # Vibration motor run time, in seconds
interval = 5   # Time between reminders, in seconds
intervalArray = [60, 300, 600, 3600] #interval options user can choose from
intervalIndex = 1
timesToTellUserAboutTiming = 0
newTimingColor = (0, 0, 255)

# Updates the number of flashes it needs to display to tell the user
# how many minutes between vibrations it has just been set to
# does not actually flash the LED in this function, instead uses tellUserNewTiming()
# to avoid sleeping and potentially missing more input and/or time to vibrate
def setNewTiming():
    global interval, timesToTellUserAboutTiming, newTimingColor
    interval = intervalArray[intervalIndex]
    timeInMinutes = interval/60
    newTimingColor = (0, 0, 100) # blue
    
    timesToTellUserAboutTiming = timeInMinutes
    
    if timeInMinutes >= 60:
        timesToTellUserAboutTiming = timeInMinutes / 60
        newTimingColor = (0, 100, 0) # green
    time.sleep(.3) #make sure it's clear a new time is being set

# Checks if the dotstar still needs to flash to tell user about a newly set time interval
# between vibrations. If there's still flashes needed, it will flash and sleep
def tellUserNewTiming():
    global timesToTellUserAboutTiming
    if (timesToTellUserAboutTiming > 0):
        #turn on for a short time
        dotstar.brightness = .2
        dotstar.fill(newTimingColor)
        time.sleep(.25)
        #turn off for a short time
        dotstar.brightness = 0
        dotstar.fill(newTimingColor)
        time.sleep(.25) 
        timesToTellUserAboutTiming -= 1 
        

def initialSetup():
    #buzz some so you know it's awake!
    vibrating_disc.value = vibrating_disc_on_value
    time.sleep(.10)
    vibrating_disc.value = 0
    time.sleep(.10)
    vibrating_disc.value = vibrating_disc_on_value
    time.sleep(.10)
    vibrating_disc.value = 0
    time.sleep(.10)
    setNewTiming()


initialSetup()
interval = intervalArray[intervalIndex]

start_time = time.monotonic()

while True:
    timer = time.monotonic() - start_time

    if timer >= interval and timer <= (interval + on_time):
        vibrating_disc.value = vibrating_disc_on_value
        if debug:
            led.value = True
    elif timer >= (interval + on_time):
        vibrating_disc.value = 0
        if debug:
            led.value = False
        start_time = time.monotonic()

    # use A2 as capacitive touch to cycle through interval options
    if touch2.value:
        intervalIndex = (intervalIndex + 1) % len(intervalArray)
        setNewTiming()

    tellUserNewTiming()
        


