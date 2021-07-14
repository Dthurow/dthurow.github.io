---
layout: post
title: Creating a Mindfulness Bracelet with Adafruit - And Remembering the KISS Principle
categories:
- technical write up
- side project
- How-to
tags:
- side project
- microcontrollers
- embedded
status: publish
type: post
published: true
excerpt_separator: <!--more-->
toc: true
---

Setting up Blinky on various microcontrollers is one thing, actually having a working embedded system is another. So, I decided I needed something relatively easy, that preferably used what I had around already, and used the conductive thread that I had recently gotten from Adafruit as a present. 

After some thinking, I came across a simple idea: I've been stressed a lot recently, and my back has been storing that all in the form of painful knots. So how about I made something that let me remember to relax my back throughout the day! I didn't want to have yet another app sending notifications, so how about something that buzzed, maybe a wearable watch? I did some googling, and came upon the [Adafruit mindfulness bracelet](https://learn.adafruit.com/buzzing-mindfulness-bracelet/overview). I already had the Gemma M0, and I could use conductive thread to sew the circuit onto a simple nylon bracelet. AND the code was obviously really simple, just wait a minute or two, then vibrate, then wait. It would be a simple and quick project to dip my toes into full embedded systems!

Or so I thought.

<!--more-->

### The Plan

Like I said, I wanted to keep it simple. I'd use the Adafruit project as a basis, but do some minor mods to make sure I actually understood what all was happening. I don't want to mindlessly follow instructions and get an end result I don't understand. The mods I wanted to do were simple:

1. **Change the wrist strap**
I didn't really like the design of Adafruit's bracelet. It just wasn't my style, you know? So I bought a cheap nylon strap from my local hardware store. I'd just sew all the components onto it, and use the buckle it came with to attach to my arm. Simple wristband with a bunch of electronics on it seemed my style.
1. **Use Coin cell batteries**
Not only did I not have the battery they recommend, I also don't really like the concept of lipoly batteries attached to me unless they're in a rigid case. I don't want them bending too much and exploding while attached to me. I'm just funny that way. So instead I decided to try my coin cell batteries. They're much better in terms of size, less explode-y, and I even have sewable battery holders that would fit perfectly on the strap
> **Future Danielle Note** This causes problems later down the way. I'm not sure how Adafruit attaches their battery at the end, but it may be worth the work if you're trying to duplicate my work.
1. **Add some code**
I'm looking to learn more about embedded systems *programming*, not just how to solder or build circuits. Using only the pre-made code seems a bit cheat-y. I knew I could add some extra functionality pretty easily, and that'd let me practice my CircuitPython as well. A win-win.

### Hardware Requirements

### Software Requirements

The basic version of the software is available on the project page here: [https://learn.adafruit.com/buzzing-mindfulness-bracelet/circuitpython-code](https://learn.adafruit.com/buzzing-mindfulness-bracelet/circuitpython-code). But where's the fun of leaving things so simple! Let's do some mods. 

The simplest change is allowing users to change how long the Gemma waits between vibrations. There isn't an easy way to let users type in a given number of minutes, but there are some capacitive touch buttons you can use. So I added the ability to cycle through a collection of times: 1 minute, 5 minutes, 10 minutes, and an hour. I attached cycling through these options to the Pad #0/A2 on the Gemma, setup as a capacitive touch button. And when the user changes the timing, they need to know what timing they've changed it to, so I need to inform the end user somehow. 

need to include libraries from: https://learn.adafruit.com/adafruit-gemma-m0/circuitpython-libraries


Use troubleshooting to determine dotstar info: https://learn.adafruit.com/adafruit-gemma-m0/troubleshooting 

Use this to connect with repl and see error: https://learn.adafruit.com/welcome-to-circuitpython/advanced-serial-console-on-mac-and-linux

screen /dev/ttyACM0 115200

Error was:
    main.py output:
    Traceback (most recent call last):
    File "main.py", line 9, in <module>
    ImportError: no module named 'adafruit_dotstar'

added dotstar library, now error:

    main.py output:
    Traceback (most recent call last):
    File "main.py", line 9, in <module>
    File "adafruit_dotstar.py", line 22, in <module>
    ImportError: no module named 'adafruit_pypixelbuf'

added pypixelbuf library, code now works


### Initial Test

It broke :(

### Understanding Battery Calculations

I haven't had much reason to learn battery calculations, aka figuring out what type of battery I need and how long they'll last. I was a web developer previously, if your laptop dies while you're looking at my site, that's a you problem. But now, it was very much my problem!

Initially I had only one coin battery on it, but that didn't work, leading to brownouts. I figure I need more juice, because the USB works fine. After double checking the adafruit docs, it turns out it needs 4-6 Volts.But one coin battery is 3.3. Why does the initial project have a 3.7V battery? No idea. But let's see if I can hack something together. I remember you can increase voltage by connecting batteries...somehow. Some googling proved I can connect two coin batteries in series to increase the voltage amount: https://www.power-sonic.com/blog/how-to-connect-batteries-in-series-and-parallel/. I do this by connecting the negative terminal on one to positive of the other. The free positive and free negative attach to the microcontroller. I used the multimeter to check the voltage before I connect to the microcontroller, and it was 5.98V, which was perfect! I gave it a whirl, and it works! But the thing is, I wasn't entirely sure why. I googled around more, but only got more confused.

I took to the local makerspace's slack, and got some lovely people to explain the concepts to me. After talking through my project and some general guidelines for calculating battery things, I came out with the following.

For figuring out voltage needed, I go through all the parts in my circuit and figure out their voltage range (i.e. look at the docs). I then make sure the voltage I provide is either inside the range of all parts, or add a part that changes the voltage before it gets to the sensitive bits, so nothing blows up.

For figuring out how long the batteries last for a circuit I haven't built yet, I'd take all power-hungry parts in the circuit, add up their current usage, make sure it's the same units as the battery's hour unit (e.g. make sure it's mA if the battery has 200mAh), and divide the mAh by the summed up mA (plus a bit for fudge factor), and that gives me a rough time it'll live.

For figuring out how long the batteries last for a circuit I have built, use a multimeter in series with the circuit, make sure I use the right setting to prevent tripping the fuse, and it'll show me the current current (har har) usage. Then divide the battery mAh by the current I see on the multimeter, and I get the rough time it'll live.

### Battery Calculations
Since I have this newfound knowledge, let's put it to good use! First step: figure out voltage. I do that by looking at all parts of my circuit, and reading their docs. My schematic-reading abilities came in handy for this, because the Gemma M0 is a microcontroller, plus other parts, so I couldn't just rely on knowing the microcontroller and going from there. Happily, Adafruit puts out the schematic info, so I could look at it, and then google part numbers to find out what each part did. 

The Gemma M0 is broken down into individual parts as understood from schematic here: [https://cdn-learn.adafruit.com/assets/assets/000/044/361/original/gemma_schem.png?1501106076](https://cdn-learn.adafruit.com/assets/assets/000/044/361/original/gemma_schem.png?1501106076). I also include the vibration motor, the only other power-hungry part in my circuit.

| part No. | Part Type | voltage range | current use | Datasheet |
|------|---------------|-------------|-----------|
| ATSAMD21E18 | 32-bit ARM Cortex -M0+ processor |  1.62V – 3.63V | 3.11 - 3.64 mA | [https://cdn-learn.adafruit.com/assets/assets/000/044/363/original/samd21.pdf?1501106093](https://cdn-learn.adafruit.com/assets/assets/000/044/363/original/samd21.pdf?1501106093) |
| ap211k-3.3 | CMOS process low dropout linear regulator | 2.5V-6.0V |  55µA when quiescent aka .055mA | [https://www.diodes.com/assets/Datasheets/AP2112.pdf](https://www.diodes.com/assets/Datasheets/AP2112.pdf) |
| AP102-2020 | APA102 IC for the three-color RGB Dimming control strip and string | .3-6V | .1W-.5W aka 20mA-100mA according to [this watt to amp calculator](https://www.rapidtables.com/calc/electric/Watt_to_Amp_Calculator.html) | [https://cdn-shop.adafruit.com/product-files/3341/3341_APA102-2020+SMD+LED.pdf](https://cdn-shop.adafruit.com/product-files/3341/3341_APA102-2020+SMD+LED.pdf) |
| 100614 | Vibration motor |  2.5~3.8V (adafruit site says 2V - 5V) | 75 mA max (adafruit site has a larger range depending on voltage, from 40mA-100mA) | [https://cdn-shop.adafruit.com/product-files/1201/P1012_datasheet.pdf](https://cdn-shop.adafruit.com/product-files/1201/P1012_datasheet.pdf) |

Looking through all of this, the voltage needs to be between 2.5 and 6 volts. And the vibration motor needs only 5V. Right now, it's connected to Vout, which is supposed to be the max power the Gemma M0 is receiving. So it may actually be getting 5.98V right now. I can check with the multimeter

For the vibration motor, because I'm turning it on and off for brief time periods, I don't want to just add the current it uses when on to the total amount, because it's only on for short times. So I need to calculate the duty cycle (percentage of time it's pulling current over a given cycle). So if it buzzes for one second every minute, that'd be 1/60, aka it's on 1.66% of the time. So if it's drawing 100mA cuz I'm giving it 5V, that means on average it's drawing 100mA*(1sec/60sec), aka 1.67mA.

>**NOTE** Duty cycle is the percentage a part is on and drawing power, for a given cycle

I have to also do this for the IC that controls the dotstar LEDs (part no. AP102-2020 in above table). This one has a max of 100mA current as well. In code, I'm turning on LEDs for a quarter of a second, to display info to end users. The max time the LED will flash is 10 times in a row (for 10 minute intervals).

Current use (taking the max current usage for some leeway) is:

(max current of SAMD21) + (max current of linear regulator) + (max current of dotstar RGB IC) + (average current of vibration motor)

3.64 mA + .055mA + 100mA + 1.67mA

105.365 mA


if the battery is 220mAh, then with this circuit, the batteries will last 220mAh/105.365mA = 2.08797988 hours


### Conclusion

### Resources

The original project: https://learn.adafruit.com/buzzing-mindfulness-bracelet/overview

This troubleshooting page explains any blinking dotstar errors you may come across: https://learn.adafruit.com/adafruit-gemma-m0/troubleshooting 

Follow this to connect with repl and see errors when the Gemma is attached to your computer: https://learn.adafruit.com/welcome-to-circuitpython/advanced-serial-console-on-mac-and-linux