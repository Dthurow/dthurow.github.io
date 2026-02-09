---
layout: post
title: Tracking Aircraft with a Software Defined Radio
categories:
- technical write up
- side project
- How-to
- SDR
tags:
- side project
- embedded
status: draft
type: post
published: true
toc: true
excerpt_separator: <!--more-->
---

Radio has always been a side interest of mine, but seemed too convoluted for me to easily get into. However, now with Software-Defined Radios (SDR), things started to shift into the software world, so I started to get my toes wet. One use that seemed pretty popular was tracking airplanes, so I thought I'd give it a go.

I had previously setup an ADSB receiver using the [adsb exchange raspberry pi image](https://www.adsbexchange.com/how-to-feed/adsbx-custom-pi-image/), and found it a little finicky. I also had other uses for the pi, so I eventually retired that setup, with the eventual plan to get it back up and running "sometime in the future". Which turns out is around now! (don't...don't ask how long it was since I did that setup the first time)

This time, I came across a different raspberry pi image that was actually default included in the [rasperry pi imager tool](https://www.raspberrypi.com/software/), called [ADSB.im](https://adsb.im/home), and decided to give it a try again. I've had it setup for about a month now (probably more once this is published!), and have learned a lot, so I thought I'd share.

![screenshot of a map with aircraft, their route, and callsigns displayed in their actual location](/assets/adsb-radio-setup/tracking-screenshot.png)

<!--more-->

## Basics for Flight Tracking

Besides looking at planes with your eyeballs, there's a variety of ways to track aircraft. The most common is looking at the ADSB data. The [Automatic Dependent Surveillance–Broadcast](https://en.wikipedia.org/wiki/Automatic_Dependent_Surveillance%E2%80%93Broadcast) is broadcast on the 1090 Mhz or 978 MHz frequency, sending out info like speed, course, altitude, callsign and identification of an aircraft. You don't even have to setup your own station to see this, you can go to [ADSBExchange](https://globe.adsbexchange.com/) or [ADSB.lol](https://adsb.lol/) to see them right now!

There's also a lot of ways to listen in on the air traffic control conversations, but that's not talked about in this article because it's not playing with frequencies and SDRs. Though I do want to mention, the Minneapolis airport has a live youtube video that shows the airport and also plays the conversations: [https://www.youtube.com/live/FY6WlMjzG2U?si=9Io45ISSSH3IGIuM](https://www.youtube.com/live/FY6WlMjzG2U?si=9Io45ISSSH3IGIuM)

## Slightly more in-depth info for Flight Tracking

To get more in-depth, sure hope you like some acronyms! The two main frequency we care about right now is the 978MHz and the 1090MHz.

**978MHz** - The 978MHz frequency is used by the universal access transceiver (UAT). UAT is intended to support not only ADS-B, but also flight information service – broadcast (FIS-B), traffic information service – broadcast (TIS-B),

**FIS-B** - is only broadcast on UAT, and provides weather info to aircraft

**TIS-B** - is broadcast on both 1090MHz _and_ 978MHz, and provides info from ground stations about aircraft that only have a basic transponder and aren't transmitting out ADSB data directly.

**1090MHz** has both Mode S and 1090 extended squitter (ES) on it. The Mode S was a replacement for a different protocol, air traffic control radar beacon system (ATCRBS). And the 1090 ES is indeed an extension of the protocol, with all the ADSB data.

If you want to play with even more frequencies:

**ACARS** - Aircraft Communications Addressing and Reporting System. Standard ACARS transmits at a frequency of 131.550 MHz. This is used for communicating between air traffic control and the aircraft.

**VDL2** - As [this article](https://www.rtl-sdr.com/receiving-vdl-mode-2-multipsk-rtl-sdr/) states: The VHF Data Link mode 2 (VDL2) is a new transmission mode used on aircraft for sending short messages, position data (similar to ADS-B) and also for allowing traffic controllers to communicate to pilots via text and data. VDL2 is intended to eventually replace the standard ACARS modes. It is found at 136.975 MHz.

## Help, My Eyes Just Glazed Over!

ADSB is messages sent out by planes and helicopters, it gives info about where they are and where they're heading. You can watch them in real time online, or setup a local station with a software defined radio, a raspberry pi, and some real simple software to glue it all together!


## Why can I see a helicopter out my window but not online?
There's a couple reasons a plane or helicopter might not be seen in an online ADSB aggregator websites. 

The LADD flag - [LADD Program](https://www.faa.gov/pilots/ladd) was created by the FAA which lets private aircraft owers to request their aircraft's flight data be removed from general distribution. Some ADSB websites follow this flag and remove the aircraft, some do not. As of this writing, I know [adsb.lol](https://adsb.lol/) still displays them.

Their transponder is off - Some government agencies (e.g. DHS) are allowed to turn off their ADSB transponders when they're in flight on various missions. This means the ADSB data simply doesn't exist to be collected! So they can't be tracked in this way.

Poor coverage - The ADSB aggregator websites are, in fact, aggregators of data, normally simply volunteers uploading (creating "feeders" like described below). If there's no one near enough monitoring and feeding the ADSB data to aggregators, it wont show up. That also means you're in the perfect place to help out the global aviation community!


## The Hardware and Setup

Hardware needed:
- [Raspberry Pi 4 model B with 1GB RAM](https://www.adafruit.com/product/4295)
- [Software Defined Radio from adafruit](https://www.adafruit.com/product/1497)
- [raspberry pi power source](https://www.adafruit.com/product/4298)
- SD card

### Initial setup
I found the [ADSB.im](https://adsb.im) website had a really good [setup guide](https://adsb.im/howto) that was straight-forward to follow. The biggest issue was simply trying to find the IP address on my network once the pi was booted up. For some reason the various auto-finder options weren't working, so I had to dredge up some old networking knowledge.

To hunt for the pi on my network, I ran `ifconfig` on my linux laptop to see what my IP address was, then did a quick ping scan with `nmap` to see who else was on my network (I knew no one else but me was connected right now)

```
nmap -sn 192.168.68.0/24
```
That quickly showed where it was living, and I went to port `80` in my browser, and success!

### How well it works

Even with the default antenna and no fine-tuning on my part, I'm getting aircraft! The pi image comes with graphs1090 data, so I can even see some more in-depth data on my system. My median range is about 11.7 nautical miles, which is about 13.4 regular ole miles. This feels pretty decent to me, and since I'm so close to the minneapolis airport, I still get a lot of aircraft even with that distance

![screenshot of graphs1090 range graph](/assets/adsb-radio-setup/adsb_range.png)

On the pi side, I can see the tracking is very low CPU usage, which is nice, I'm not burning up the whole pi trying to do anything too fancy.

![screenshot of graphs1090 cpu utilization](/assets/adsb-radio-setup/cpu_utilization.png)

I also enabled skystats (more below), which increases IO writes, and boy can you see that in the disk IO graph. I assume at some point that will fry the SD card in my pi, but for now, I'm fine with being rough on it in exchange for fun info about planes.

![screenshot of graphs1090 disk IO graph](/assets/adsb-radio-setup/disk_io.png)

### Fun configurations

In the Setup -> Advanced setting on the website, you can enable SkyStats

![Screenshot of the Advanced settings page](/assets/adsb-radio-setup/Advanced-setup-skystats.png)

[Skystats](https://github.com/tomcarman/skystats) is a docker container you can run on the raspberry pi that watches the ADSB data coming in and collects various stats, and of particular interest, flags interesting aircraft using a local copy of [plane-alert-db](https://github.com/sdr-enthusiasts/plane-alert-db), which lists interesting aircraft and why they're interesting. It also hooks into various airplane photo websites, like [jetphotos.com](https://www.jetphotos.com/) to give you pictures, even if you missed seeing it yourself as it flew by.

There's a lot of other configurations I haven't even touched on the pi, but that's a future todo for now.

## Interesting Planes

I've never really noticed planes outside of the constant stream of Delta flights heading out from the airport, so it was fun to see models I'd never heard of before. Here's a couple that stuck out.

### Short SkyVan

I've never heard of this plane before, but when I was poking around at SkyStat's interesting airplanes, this just made me laugh. Look at this ridiculous plane!

![Picture of the Short SC.7 Skyvan airplane. It is light grey, with a snub noise and a very square-looking body](/assets/adsb-radio-setup/win_aviation.png)
(Image taken from jetphotos.com)


Looking into who owns it and what it's for, it's apparently for training paratroopers and owned by a defense company to help military training. So, maybe not so funny. But it still looks ridiculous. It flew over Minneapolis back on february 8th

[Route on adsb.lol](https://adsb.lol/?icao=a18435&lat=45.221&lon=-93.803&zoom=6.2&showTrace=2026-02-08)

### 747 Dreamlifter

Skystats tags this as "Absolute Unit", and you know what, it sure is.

![Side view of a boeing 747. However, the top of the main area that normally has passengers bulges upwards, making the body of the aircraft about twice as high](https://cdn.jetphotos.com/full/5/63687_1630935322.jpg)

The Boeing 747 dreamlifter was designed to be able to ship the Boeing _787_ parts between Italy, Japan, and the US. And it appears that's exactly what it was doing, flying from Japan, to anchorage, down to Charlston, flying over Minneapolis en route. 

[Route on adsb.lol](https://adsb.lol/?icao=aa90a0&lat=42.598&lon=-93.155&zoom=5.5&showTrace=2026-02-04)

## Next steps

Some next steps I want to do:
- Learn more about antenna selection. That apparently can make a huge difference in range, but I just have the stock antenna for my SDR.
- Hook into other sources - ACARS and VDL2 could be interesting to listen in on, and it's apparently possible with an SDR. Maybe I should get a second one to complement my ADSB listening?


## Resources

Build your own feeder:
- [ADSB.im raspberry pi image](https://adsb.im/home)

Watch planes online:
- [ADSBExchange](https://globe.adsbexchange.com/) 
- [ADSB.lol](https://adsb.lol/)

Some interesting other things to do while tracking aircraft:
- [Receiving Airplane data with ACARS](https://www.rtl-sdr.com/rtl-sdr-radio-scanner-tutorial-receiving-airplane-data-with-acars/)
- [Receiving VDL mode 2](https://www.rtl-sdr.com/receiving-vdl-mode-2-multipsk-rtl-sdr/)

Fun plane data:
- [Skystats](https://github.com/tomcarman/skystats)
- [plane-alert-db](https://github.com/sdr-enthusiasts/plane-alert-db)