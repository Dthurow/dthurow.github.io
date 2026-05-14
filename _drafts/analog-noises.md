---
layout: post
title: Analog Noise Machines
categories:
- technical write up
- side project
- How-to
tags:
- side project
- embedded
status: draft
type: post
published: true
toc: true
excerpt_separator: <!--more-->
---


You ever feel like you just want to make some noise? Maybe a horrendous noise? And you want to use electronics to do it? Well do I have some fun projects for you, lets dive into the world of super simple analog noise makers!


TODO: Add pic here

<!--more-->

# Overview

Nowdays most intro-to-sound tutorials will have you grab an arduino or other microcontroller and a speaker, but _back in the day_, things were still analog. No computer, just a bunch of electrical components to use (or abuse) to create oscillating voltages with different frequencies to make sound. 


# The most basic - Super Simple Oscillator

Probably the simplest I've found is this super simple oscillator from [Look Mum No Computer](https://www.lookmumnocomputer.com/simplest-oscillator/). This is created by abusing a poor transistor who didn't hurt nobody. 

TODO: Schematic from the link here

## How it works
The basic concept has you hook up a transistor's collector and emittor backwards in the circuit, in parallel with a capacitor, and a resistor in series. The battery charges up the capacitor while the transistor basically has nothing flowing through it because it's backwards. Once the capacitor reaches the right level of voltage, though, it triggers an "avalanche" in the transistor, where it suddenly has very low resistance. The capacitor discharges through the transistor until its voltage is lower than that trigger point, and the circuit goes back to its original state, with the capacitor charging up. This repeats, and you get some oscillation, and therefore, noise! If instead of a single resistor, you do a resistor plus potentiometer, you get the ability to control how fast the capacitor charges, and therefore the frequency of the oscillation.

The fun part of this circuit is 

- if you have any sort of component collection, you probably already own all the parts for it (I did!) 
- exactly which value of each component is super loose. You can use different NPN transistors, which will trigger at different voltages. You can use different sized capacitors, which determine the baseline frequency your pot is changing. You can add an LED, or not. 
    
After playing around with it, it kind of felt like you could just throw a handful of random components on it, and it'd somehow still oscillate. Fun stuff!

However, there's definite limitations to what sort of sounds you can get out of it. So let's go a little bigger.

# Next Step Up - Atari Punk Console

While it's not individual components, a classic 555 timer chip counts as analog to me. So how about two of them? Lets build the Atari Punk Console. 

> **NOTE** There's a _lot_ of different circuits and walk throughs online. If you want to see how variable they can be, it's fun to compare the circuits with different values and compare/contrast. Well, fun to me, anyway.


## How it works

I ended up using the circuit from this website: 
[https://www.build-electronic-circuits.com/atari-punk-console/](https://www.build-electronic-circuits.com/atari-punk-console/)

Mainly because it included some resistors that other versions lack. For example without, look at [the circuit this user built on electronics stack exchange](https://electronics.stackexchange.com/questions/102592/problems-with-atari-punk-console-circuit ). This version of the Atari Punk Console has the second potentiometer conect the power source to pin 7 on the second 555 with no resistor in series. So if the potentiometer is turned all the way down, the resistance is 0 and the pin is getting full power. So when the 555's internal transistor discharges through the chip, it's just shorting out.

> **Fun Fact** Creating shorts across your battery is not good!

The linked stack exchange talks about what happens then, the timer gets very hot or even melts. Not so good for music making.

Throwing in a few resistors so there's always _some_ resistance on the connections between power and the potentiometer seemed like a good thing, so I went with that version.

## My Build

After spending a concerningly long time at our local surplus store with a huge electronic component selection ([Ax-man surplus](https://www.ax-man.com/), how I love you), I had everything I needed.

I translated the schematic to a breadboard for initial testing, and then converted it over to a perfboard with soldered connections for a more permanent setup. 

TODO: ADD PICS


## CV Control

The 555 chip has a CV pin right on it, pin 5, which isn't used at all for most atari punk consoles I've seen. However, it is possible to add that functionality pretty easily. This allows you to add some audio jack plugs that, when connected to an appropriate synthesizer module, can control the exact tone you get. The addition is shown below.

TODO: ADD PIC

As you can see, it's adding a vactrol connected to an audio jack on one side, and the CV voltage pin on the other. The vactrol is just a photoresistor and an LED, so as the voltage goes up, the LED gets brighter, and the photoresistor changes resistance. The end result becomes: "Voltage change from the CV input results in a voltage change on the CV pin". But with bonus that it keeps the atari punk console isolated from whatever is plugged into the CV input jack, since only light is being sent between the CV jack and the atari punk console. 

## Final Results

TODO: ADD SOUND?

From reading my scope across the speaker, the output seems to be about 4.8 volts peak-to-peak, but with a RMS value of 119.8mV. 

# Resources

TI's 555 timer documentation: [https://www.ti.com/lit/ds/symlink/lm555.pdf](https://www.ti.com/lit/ds/symlink/lm555.pdf)