---
layout: post
title: CanSecWest Review
slug: cansecwest-review
categories:
- Conference
- Review
tags:
- cansecwest
- security conference
- review
status: publish
type: post
published: true
meta: {}
---

As I mentioned in a previous post, I went to two security conferences several weeks ago. I already posted a review of the first one I went to, Bsides Vancouver. This post will be about my thoughts on CanSecWest, the second conference in BC. (
[https://cansecwest.com/](https://cansecwest.com/) )

I was fresh off my first conference, and took an early night, figuring I’d need it in the morning. I’d gotten a discount through CanSecWest, so I was actually staying in the hotel where it was happening. (It’s so nice to be able to hide out in my hotel room whenever I felt like it.)

CanSecWest markets itself as “the world's most advanced conference focusing on applied digital security”. They have their conference at the Sheraton Wall Centre in downtown vancouver BC, only a few blocks away from where the BSides Vancouver conference was held. For a full list of speakers and their talks, check out: 
[https://cansecwest.com/speakers.html](https://cansecwest.com/speakers.html). Trying to get a training request in for this conference was a pain and a half. They didn’t put up their official speaker and agenda list until just a month or two before the conference, which is kind of a pain when your training request needs to wend its way through your company's internal process before you can  even start to register and pay for everything. I did end up mentioning this to a few other people at the conference, and they all said this was pretty common. Apparently, some hackers enjoy totally messing with the guys trying to run the conference, which can lead to some wonkiness. For example, the conference opened with them showing us how somehow, a fresh out-of-the-box computer trying to boot from a USB was being owned by someone. They were explaining how that’s why the wifi was pretty sketchy for most of the conference. So if you’re particularly paranoid (or really, just slightly paranoid), I’d suggest sticking to pen and paper until the end of the conference, just to be sure.

But now that we’ve covered the basics there, what about the actual talks?

Like for my BSides review, I’m not going to go in-depth on each of the talks. If you’re really curious, they have a lot of the slides from previous years at: 
[https://cansecwest.com/slides.html](https://cansecwest.com/slides.html) that you can go peruse. Instead, I’ll just mention a few that I liked.

One particularly fun one was “Low cost radio wave attacks on modern platforms” by Mickey Shakatov and Maggie Jaurequi from Intel. In this talk, they basically did a bunch of demos with just a cheap hand-held walkie-talkie, showing how it can totally mess with a bunch of different computer systems. A couple of the examples I remember off the top of my head: making the plugin part of a hairdryer spark and explode, making chips in a computer jump by a 100 degrees, and making another computer just straight up turn off. They didn’t go into technical details about why exactly this happened, it was a more hands on, “look at this crazy stuff that can happen” sort of thing. It was super interesting to watch, and definitely made me more curious about what’s really going on. (Also really tempted to buy some walkie-talkies, turn them on next to a variety of electrical equipment, and seeing what happens. But that feels like a bad idea for some reason…)

Another that I enjoyed was “Inside Stegosploit” by Saumil Shah. This one talks about a process of encoding a javascript exploit into an image, then having it so, on load, the image pulls out the exploit script and runs it. It’s a pretty slick set-up.

The stegasploit stuff uses two main pieces to put it together: one, encoding javascript into the image, and two, getting the image to work both as an image file, and a html file (aka, making the image something called a “polyglot”).

I haven’t played around with image files that much, so it was a quick lesson on how the images are actually stored (e.g. as multiple different layers), and how we can use that to hide the javascript info inside the image. The second part was also super fun. Because we’re all constantly adding to different formats and specs, most file formats are designed to be extensible later on. So some formats will essentially say “and then there’s this variable length field that can be used for whatever” so that way if something cool pops up in the future, they can tack on an extra field (like “a field called enableVR set to 1 will hook you into the matrix” or something) without making all the old files in the old format obsolete (that whole “backwards compatibility” thing). So this means that we can use this space for whatever. Like, say, including an entire html page inside that piece. There’s some clever tricks to make it so a file can be loaded both as a valid image, and as a valid html page, and several other bits that are needed to make everything work, and it was just a fun and interesting talk.

There were several other ones I found interesting and enjoyable that I’ll touch on just briefly. There was a talk about election voting machines, and how they are just hilariously not protected in the least in so many different ways (and how you too can buy official state of michigan stickers to make your fake voting machine look totally legit). Another one talked about different possible ways to detect hacking and shenanigans inside a car, by trying to add on to the main CAN bus, and another talked about how Advanced Persistent threats (APTs) can squat on domains that are just a typo away from a valid domain in order to mess with and hack people who are the victims of fat fingers.

These are the ones I felt I understood pretty well, and enjoyed on a technical level. However, there were also quite a few that I felt were way over my head, dealing with understanding a lot of very low-level details I feel I’m just not there yet on. For the most part, they made me want to get more into reverse engineering and assembly.

CanSecWest also had some vendors in the area outside the main hall where the talks were being held, and I had some interesting chats with them while waiting for the talks to start. Tesla was there, trying to recruit pen testers to test their cars, which sounded super fun. Google, Microsoft, and Adobe were all there as well, giving away free swag (I swear Google’s guys didn’t even try to pitch working at Google to us. It was like “everyone here knows Google, it’s fine. Just take the free stuff”. Got a bit of a laugh out of that.) Since I’m a total noob in the security world, it was fun talking with the vendors and learning more about who’s who in the security world, and especially the security world around the Vancouver area. However, they definitely weren’t the focus point. You want to talk to a bajillion vendors, apparently RSA or some other conference would be best. This one was focused on highly technical and highly interesting talks, and it was quite enjoyable.

So, to wrap this all up, let’s do some “why you should/shouldn’t go” lists, and a tl;dr.

 

Why you should go to CanSecWest:

* You think reverse engineering a modem is a good day of fun


* You want to meet fellow people who think using the specs for a specific file format for evil is a fun and enjoyable hobby


* You want some very expensive hands-on training (they offer “dojos” hands-on training during the week before the conference. They’re super expensive though, so I didn’t go to any. They sounded pretty solid though)

 

Why you should NOT go to CanSecWest:

* You’d prefer point-and-click security tools you don’t have to think about


* You want to get a bunch of vendors to give you free swag (there’s only so many times you can go back to the one Google vendor to get free Google socks before the guy starts giving you funny looks…)


* You’re a beginner computer programmer (Some of the talks are higher-level, like the ones I mention above, but for the most part, they expect you to dive in and hold on. I think it’d be too much for a total newbie)


* You’re paying for it for yourself (It’s just so expensive… I mean, if you’re rich or whatever, then I guess you could go for it. Otherwise, it’s just too spendy.)

 

**Tl;dr** 

CanSecWest is a highly-technical security conference that focuses on in-depth examinations of people’s exploits and hacks. There are some high-level stuff, but it’s pretty bare. If you can get your company to pay for it, it’s a great and cool place to go.
