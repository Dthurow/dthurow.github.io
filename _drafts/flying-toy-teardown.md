---
layout: post
title: Flying Toy Teardown
categories:
- technical write up
- side project
- How-to
- reverse engineering
tags:
- side project
- teardown
- embedded
status: publish
type: post
published: true
meta:
  _thumbnail_id: '34'
---

I've recently (and finally) got my electronics lab more set up in my basement. And that means I was itching to put it to use. So I decided to take apart a flying toy that had been hanging about for about a year. I got it after my boss had bought them and brought them into the office for about a half hour of fun, and then for some reason, I took it home. I don't remember why anymore, so hopefully I didn't steal them... if I did, sorry Jill, I'll pay you back!

![The Flying toy I'll be breaking down](/assets/flying-toy-teardown/20210517_154616.jpg)

## The Basics

So this toy is relatively simple. There's an on/off switch. When you flip it on, it waits for a couple seconds, then the rotors start going and it lifts off. It will slowly sink downward until it gets close to the ground, then suddenly rev its engines fly upward. This can cause problems if there's exposed ceiling beams that it gets on top of, which would cause it to stay flying out of reach. Definitely not speaking from personal experience, there. It can also be recharged with the micro USB plug on the bottom of the ball. And lastly, it has several LEDs. When it's charging or low battery, the ball lights up in red. When it's turned on and flying around, it has 3 colors, red, blue, and green. So with all that initial work, here's a diagram of the system with my current knowledge.

![Flying Toy diagram version 1](/assets/flying-toy-teardown/FlyingToyDiagramV1.png)

There's a lot of unknowns/questions here. I'll need to tear it open to find out more. So lets go!

![Flying toy is slightly opened along a seam running down the middle of the ball](/assets/flying-toy-teardown/20210517_154641.jpg)
Managed to crack it open along the length of the ball, but the bottom seems stuck closed

![Flying toy angled slightly to see a small hole in the casing. Down deep inside there is a single screw](/assets/flying-toy-teardown/20210517_154954.jpg)
Looks like a screw was holding it close. Close investigation showed there were actually two other screws that were supposed to be holding it close where I opened it, but the plastic just gave out. So after trying to use a screwdriver, I decided to just brute force it open. 

![The flying toy is open. There is a small PCB board and a battery](/assets/flying-toy-teardown/20210517_155235.jpg)
Success!

### The battery
First thing you can see is about the battery is the lovely little plastic holder it slots into. That's a nice way of keeping it out of the way and stable! It seems to be a standard Lithion Ion poly battery, pretty common in small electronics. They're also best used when you know they're not gonna get beat up (like inside a plastic ball). If they get punctured or bent too far, they can get a bit explosive. Happily, youtube has many videos to demonstrate what happens. [Here's one](https://youtu.be/wUFxlf4fXjo)
The battery helpfully prints the voltage and charge on the casing, so it's easty to tell it's 3.7V and 75mAh. That's a real small battery! The smallest battery I can find on adafruit is 100mAh. 

![Close up of the battery. It has voltage and charge stamped on the casing](/assets/flying-toy-teardown/20210517_155511.jpg)


The battery is also rechargable. When this one is plugged in with USB, a LED lights up. This indicates to me there must be some brains behind the charging process. When I start looking at the chips on the PCB, I'll keep an eye for anything that looks like a charger of some sort. 

### The proximity sensor
When the ball was closed, there were two things sticking out. One looked like a classic LED, and the other was a black piece of plastic. Opening it up, you can see they're both attached to the PCB. Now, I've played with infrared sensors before, and the bit of black plastic looked an awful lot like an IR sensor. Couple that with a possible IR LED, and I think I got the proximity sensor figured out. The ball has a IR LED that's lit up. When the toy gets close to the ground, the IR bounces off the ground and hits the IR sensor, which triggers the motor to run faster and lift the toy off the ground. 
How to test this? Well, IR shows up on camera! I tried just taking a video, but the other regular LEDs really made it hard to see if the potential IR LED was lit up or not. So instead, I pulled out a random remote that I had lying around. When I press a button, the IR LED on the front of the remote lights up. If I covered up the potential IR LED, I could prove the black piece of plastic was an IR sensor. I set everything up, and sucess! The remote could turn the flying toy on and off. 