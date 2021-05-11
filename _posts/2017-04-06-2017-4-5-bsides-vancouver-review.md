---
layout: post
title: BSides Vancouver Review
categories:
- Conference
- Review
tags:
- Bsides
- vancouver
- security conference
- review
status: publish
type: post
published: true
meta: {}
---

A few weeks ago, I went to two information security conferences in Vancouver BC, Bsides Vancouver and CanSecWest. I’d stumbled upon the conferences while browsing online, and on the off chance I could convince work this was work related, I applied for training so I could go. Surprisingly, it was okay-ed, and I was sent on my way. (If you are from work and were one of the people who okay-ed, it most definitely was related to work. Pinky-promise.)

Bsides Vancouver is part of the security Bsides group of conferences. They’re less formal than normal “official” conferences, and they’re often organized by the security community from the local area. Bsides Vancouver was a two day affair on Monday and Tuesday, in downtown vancouver at 560, a night club, funnily enough. It felt enjoyably surreal to be listening to a talk about state-sponsored attackers and how to protect your company from certain attacks, all the while having a disco ball slowly rotate above you.

The talks were pretty diverse, you can find the exact list on the Bsides Vancouver website. ([https://bsidesvancouver.com/](https://bsidesvancouver.com/)). However, there were a few that stood out for me personally, so I’ll mention them specially here.

First was the “Powershell Hacking for Fun and Profit”, by Guy Rosario. He’d created what he called a purple team mind-map for powershell. Basically, it was a gigantic cheat sheet of different powershell commands that you’d use when doing a red team penetration test, or blue team defense work(get it? red+blue=purple. Security people are so clever). He also had commands that would be helpful for computer forensics. He didn’t go too in-depth of the exact commands, instead giving a high-level overview of the different commands and powershell frameworks that he’d documented in the tool. I’ve used powershell some at work, mainly for doing bulk movement of files, so it was fascinating to see how powerful it was. He also said that BSides would get us a link to his project, but so far, I haven’t seen it online or in an email from them, and googling hasn’t turned up much help. I assume the organizers are still recovering from running the conference, and I’ll hear from them soon.

Another enjoyable one was “Around the World in 80G”. This talk was from Richard Henderson, who works with the company Absolute. I’d never heard of them before, and what they do is both really cool and kinda creepy. They have some code on most BIOS’s, called computrace. Businesses can turn it on, and it allows Absolute to do a variety of things on that computer: take screenshots, turn on the webcam, or completely lock up the laptop. This is so if the laptop is stolen from work, they can turn on the program, and take pics of the criminal in action, as well as (hopefully) track them down.The special bit is that since they’re in the BIOS, wiping the OS doesn’t matter, because it’ll re-install in the OS on the next boot-up. Like I said, cool idea, but kinda creepy knowing it may be on your computer (I looked on mine, it did have it, as well as some radio boxes that let you disable it. This apparently disables it forever and “can’t be undone”. I’m skeptical on this, but will believe it for now).

All this was just the preamble for the talk, though. With that info explained, the speaker went on to talk about different cases that they’d dealt with. Stolen laptops got shipped across the US, or across the world. They also were often stolen by incredibly stupid people, apparently. People who would steal a laptop,  would then log into facebook or their personal email, or take selfies with the webcam. They also had several stolen phones, apparently, where the criminal would then take selfies, or my personal favorite, take pictures of themselves with their buddies, smoking weed and going over 100mph in their car. Police tend to frown upon that sort of thing, so I’ve been told. All-in-all, a fun talk learning about something I’d never heard about before.

Funnily enough, when I was taking the train back from my conferences, I ended up sitting next to another guy who worked at Absolute. He didn’t even know somebody from his company had done a talk at BSides, he just happened to be taking the train down from BC to one of their satellite offices. He struck up a conversation and we had an enjoyable chat down (Even though he
wasan ops guy, and I’m a dev. But I didn’t hold it against him, and he didn’t seem to hold it against me either, so it worked out alright). But I digress from conference.

Besides their talks, they also had a small lockpick area next to a few vendors, away from the rooms with talks, where people could mingle and chat. They had a nice spread of locks and lockpicks on a small coffee table with some couches sitting around it. Since they had several “social breaks” and an hour long lunch, I took the chance to get some hands-on practice. That was quite enjoyable, and I’d never really played with lockpicks before (hey, I was always a goody two-shoes growing up, don’t judge). I managed to pick the 2 pin lock, and the 3 pin once. They had a couple sets of handcuffs, too, which were shockingly easy to pick (at least, when you weren’t wearing them. I was too chicken to do them on my wrist, though some people managed it.). The funniest bit, however, was when one guy decided to try picking the handcuff while it was on his wrist, but it went slightly awry. Unfortunately for him, someone else had managed to break part of a lockpick inside that cuff, and hadn’t told anyone. This rendered the lock both unpickable, and unlockable. period. He had to have the cuff on for about a half hour, until they finally got him loose. A good rule of thumb there: if you’re picking locks, maybe make sure nothing bad is going to happen if you can’t get it unlocked (or embarrassing, as was his case).

I won’t go into too many other talks that happened at Bsides, or the different conversations I had, since I still have another whole conference to talk about (which I’ll talk about in my next post), but I will wrap this up with a few overall opinions. And because I’m a list sort of person, they’ll be in list format.

 

Why you should go to Bsides Vancouver:

* You want to meet cool security people in Vancouver BC (met a couple pretty cool people)


* You want to learn more about different areas in security you wouldn’t have heard about otherwise


* Learning about tools you’ve never heard of (there apparently 50 billion different powershell frameworks, which I didn’t even know was a thing)


* You can also start meeting up with people in MARS, the group that threw the Bsides. I guess they have informal meetups every month that sound pretty fun (though too far for me to go to just for a night of drinking and hanging, at least for now.) More info on them:[https://fourthplanet.ca/](https://fourthplanet.ca/)


* Talk with people who truly understand the pain of javascript (I may have vented to someone else who said they did web development too. They felt my pain)


* They’re hecka cheaper than most other conferences (Their basic entry price was 60 buck Canadian, pretty nice)

 

Why you shouldn’t go to Bsides Vancouver:

* You’re hoping to become a 1337 haxor (I’m
prettysure I didn’t meet anyone like that. At least not anyone who would have used the term “1337 haxor” seriously...)


* You want in-depth training on stuff (the talks seemed high-level and/or interesting, not necessarily in-depth and hands-on. They did have one with some hands-on, but I didn’t end up going, so not sure how that went)


* You’re super introverted (I’m pretty bad at that, and I’m also pretty sure I had an almost-claustrophobic/panic attack thing going on towards the end of the first day. The venue was very echo-y, and with over 300 people in there, all talking loudly, it can get to you if you’re not used to it)

 

I'll post a write up shortly on CanSecWest, but till then, a tl;dr for Bsides:

**Bsides Vancouver is a fun and interesting conference, with high-level talks about all sorts of security related stuff. While the venue had some pros and cons (pro:disco balls, con: echo-y nightclub), I’d definitely recommend it if you live in the area.** 

 
