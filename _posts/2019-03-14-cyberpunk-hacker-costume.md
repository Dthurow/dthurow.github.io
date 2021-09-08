---
layout: post
title: Halloween 2018 - Cyberpunk Hacker
slug: cyberpunk-hacker-costume
categories:
- side project
tags:
- python
- costume
- side project
- embedded
status: publish
type: post
published: true
excerpt_separator: <!--more-->
meta:
  _thumbnail_id: '14'
---

This last Halloween I decided to pull out all the stops and finally use my Adabox tech (
[https://www.adafruit.com/adabox](https://www.adafruit.com/adabox)) to make a fun CyberPunk Hacker costume for my work’s Halloween costume competition. After a quick trip to Goodwill and Value Village, I had some suitably punk-style clothing. I got some spray-on blue hair dye (and a lot of hair gel) and all I needed was some cool looking tech to complete the outfit. Below is a short write up of my tech and code, with links to the code on github. None of the code is super polished, since I did all of this over a long weekend right before Halloween, but it certainly works. And I gotta say, work feels a lot more fun when you’re in full hacker gear, even when you’re just debugging a weird JavaScript bug.








  

    
  
    
![HACK THE PLANET!!](/squarespace_images/image1.jpg)
    <!--more-->


  



## “Hacking” device


You can barely see this device on my left hip in the picture. This is just a plain a circuit python express playground from adafruit (
[https://www.adafruit.com/](https://www.adafruit.com/product/3333)[product](https://www.adafruit.com/product/3333)[/3333](https://www.adafruit.com/product/3333)). I took bits and pieces of different example python scripts plus my own pieces so I could “hack” my coworkers computers. The express playground has multiple capacitive touch points, which I used as buttons to turn on and off the Neopixel LED next to it.

Once powered on, my code would run a simple loop that would:

* Turn on/off the LEDs


* If certain LEDs were on, play a light sequence and a sound clip (for this costume, either flashing green with “System accessed” sound clip or flashing red with “Accessed Denied” sound instead)

Since the express can be powered by USB, I bought a retractable USB cable, and had it just hang off the express. I also used a magnetic clip on the back to clip it to my belt.

Github link to code: 
[https://github.com/Dthurow/CyberpunkCostumeCode/tree/master/HackingDevice](https://github.com/Dthurow/CyberpunkCostumeCode/tree/master/HackingDevice)

So the end result is I had a small circuit board that I whip off my belt, plug into somebody’s computer and press a few buttons, then voila, have it flash green while saying “System accessed”! I’ve hacked their systems!


 
   

 


## Light up glove


This is yet another Circuit Python Playground express! I added some python and shoved it under one of my gloves, with a USB cable going from the micro USB port, up my sleeve, and down into my pocket where I had a small power brick.

The code for this used the two click buttons on the top of the playground express, the NeoPixel LEDs, and the microphone.

I had multiple different states that I rotated through using the two click buttons. The different states were:

* Off - self-explanatory


* Rotating rainbow - All the NeoPixel LEDs were on, with each of them slowly changing colors so it’d look like a rainbow rotating in a circle


* Loading Rainbow - only half of the NeoPixel LEDs would be on, instead they each turn off and on in the classic “loading please wait” action, with each full rotation triggering a color change through the rainbow


* Voice detector - This uses the built-in microphone and the NeoPixel LEDs. The louder the noise, the more lights it lights up.

Github link to code: 
[https://github.com/Dthurow/CyberpunkCostumeCode/tree/master/LightUpGlove](https://github.com/Dthurow/CyberpunkCostumeCode/tree/master/LightUpGlove)


 
   

 


## Programmable light sling bag


This one is probably the most amount of hardware, with a NeoPixel LED programmable strip (
[https://www.adafruit.com/product/3919](https://www.adafruit.com/product/3919)), the adafruit hallowing (
[https://www.adafruit.com/product/3900](https://www.adafruit.com/product/3900)), a little ohm speaker (
[https://www.adafruit.com/product/3923](https://www.adafruit.com/product/3923)), and an actual battery (
[https://www.adafruit.com/product/3898](https://www.adafruit.com/product/3898)).

This one’s code re-uses the concept of multiple states I can rotate through. This time it uses the two capacitive touch points on the hallowing. One turns it on and off, and the other rotates through several possible states which I’ve informally named:

* Loading Blue - Neopixels are all turned off, and starting from the bottom going up, the next LED turns blue until all are on and then restarts the loop


* Flashing Green - flashes all the LEDs on as green, then off in a loop


* Party Mode - All LEDs flash in one of the colors of the rainbows, then off, then another color of the rainbow, while the speaker played free techno/rave song at full blast.

Github link to code: 
[https://github.com/Dthurow/CyberpunkCostumeCode/tree/master/HalloWing](https://github.com/Dthurow/CyberpunkCostumeCode/tree/master/HalloWing)


 
   

 


## Arm hacking device


Last and certainly least, my hacking display on my arm. This feels like a bit of a cheat. I got a cheap phone holder that goes on your arm, slid my phone in, and went to 
[http://geektyper.com/mobile](http://geektyper.com/mobile) in chrome so it’d full-screen. It has a nifty option “Auto” which just constantly displays new gibberish “hacking” text on the screen. But I do feel it adds the proper level of ambiance to the whole thing.



## Conclusion


So there you have it, my cyberpunk hacker costume revealed. I ended up tying for third at my work’s costume competition, which I was quite proud of. And playing with Circuit Python was a lot of fun. Really, the biggest downside to this whole thing?

How on earth am I going to top this for next Halloween…
