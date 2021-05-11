---
layout: post
title: 'WarGames: Learning hacking (security) the fun way'
categories:
- Talk Write Up
tags:
- ctf
- picoctf
- microcorruption
- over the wire
- talk
status: publish
type: post
published: true
meta:
  _thumbnail_id: '17'
---

**Tl;dr**
I gave a talk last year on wargames, hands-on security learning websites, and wanted to make a blog version of the talk. Wargames are fun puzzles that teach you security concepts by hands on learning and self-guided research. With no time-pressure or required competition, they’re a great way to get started learning security in a stress-free manner.

**Intro**








  

    
  
    
![Bellingham Codes - Wargames (6).jpg](/squarespace_images/Bellingham+Codes+-+Wargames+%286%29.jpg)

  


  



At the end of last year I put together a short talk at the local tech meet up, Bellingham Codes (
[https://www.bellingham.codes](https://www.bellingham.codes/)). I figured I should do a write up version of the talk as well. The talk title is the same as the title of this post. Wargames: Learning hacking(security) the fun way. Now, the easy way to theme the talk would have been referencing the movie Wargames. However, because I like Hackers more and I was the one giving the talk, I chose to theme it that way instead. So without further ado - Wargames!

**What Are Wargames?**








  

    
  
    

![Bellingham Codes - Wargames.jpg](/squarespace_images/Bellingham+Codes+-+Wargames.jpg)
  


  



Wargames in the security world are websites that have long-running security challenges. You can sign up and try your hand at a wide variety of security-related challenges, from a simple cross-site-scripting to reverse engineering a program. Some wargames, like the examples I’ll give later, were originally capture-the-flags (timed, competitive security puzzles/challenges) that the hosts were nice enough to leave up for an indefinite amount of time. Other wargame sites were originally designed to simply run forever, sometimes with rotating challenges to keep the sites fresh and interesting. 

Because they’re related to capture-the-flags (CTFs), they can have systems in place so you can compete with others on the site, but often that’s not a requirement. For the anxious, this makes them a lot less stressful than CTFs. They also often have systems in place so you can play the wargame either as an individual, or as a team, which is also a set up borrowed from CTFs.

The two main formats of challenge sites are Jeopardy and attack-and-defense style. Jeopardy style is pretty simple. The challenges on the sites are a series of questions, and the “answers”  are normally flags (strings of gibberish) that prove you’ve solved the question. Examples for that would include something like “The flag is stored in the given text file, next to the sequence ‘hello world’”. You’d then have to search through the text file for the sequence ‘hello world’ and find the flag next to it, then submit that flag to the site. 

The other style is attack-and-defense. I don’t have as much personal experience with these, so I’ll keep this brief. This style has one person designated the “attacker”, and another a “defender”. The attacker must attack a specific system, while the defender tries to stop them. Often, the attacker of one system can be the defender of another at the same time. This is a common CTF style, but the wargames I’ve found tend to be jeopardy style.

Now, what exactly will these challenges actually be about? Well, there’s pretty much a wargame for every aspect of security and computers in general. There’ll be wargames focused on linux command line (e.g. overthewire bandit, explained more later), cryptography (decrypt the given string is a common challenge), web applications (access a hidden webpage), and more.

Basically, if you’re a hands on learner, and want to learn security, wargames can introduce you to everything you could possibly want.

**What do you need?**








  

    
  
    

![The image there should be a gif, this one  https://bit.ly/2ORo1cV](/squarespace_images/Bellingham+Codes+-+Wargames+%282%29.jpg)
        
          
        

        
          
          
The image there should be a gif, this one 
[https://bit.ly/2ORo1cV](https://bit.ly/2ORo1cV)
  


  



Now, if you’re interested in wargames, what all do you need to actually, you know, play them? Most of what you need is pretty simple. An internet connection and a computer is the bare minimum, I have yet to see a completely offline wargame (though I’m sure they exist). Because you’re going online, I’d also suggest a VPN of some sort. If you’re not sure what VPN to use, I’d suggest looking at: 
[https://thatoneprivacysite.net](https://thatoneprivacysite.net/). 

Some wargames are based entirely in-browser, and are fine accessing directly on your computer. Others require you to log in to shared accounts, or use a VPN to access vulnerable computers, and in that case, I’d strongly suggest using a virtual machine (VM). You can spin up a VM running linux pretty easily with VirtualBox. I won’t go into how, but there are a lot of nice tutorials online if you look around. VMs are nice because you can create an up to date operating system, save a snapshot of it, do what you want, then revert the entire OS back to the original snapshot. For some wargames, you’ll be connecting to systems that are accessed by a lot of curious new hackers, so having some protection from accidental or malicious hacking of your system seems pretty common sense. If all this feels too scary to mess with, then you can ignore all this and only do wargames that are in-browser only, like Microcorruption below.

**Examples**








  

    
  
    
![Bellingham Codes - Wargames (3).jpg](/squarespace_images/Bellingham+Codes+-+Wargames+%283%29.jpg)

  


  



First wargame example is Over the Wire (
[https://overthewire.org/wargames](https://overthewire.org/wargames/)). They have a collection of wargames made either by their community or ported over from an old site, and there’s a lot to learn and keep you busy there. Their intro wargame is called Bandit, and I think it’s a lot of fun. Bandit is an intro wargame that teaches the basics of navigating a linux system via the command line, building and scheduling bash scripts, as well as basic networking concepts. 

In Bandit, you ssh into their system (connect to a remote computer using the command line), starting with username/login of bandit0/bandit0. Each level has a hint telling you where and how to find the password for the next level’s user (so level 1’s username is bandit1, level 2 is bandit2, etc). While they don’t hold your hand (they expect you to read the manual and search the internet for info) they do provide hints on what linux commands you might find useful. This makes it a lot more fun to learn command line tools than simply reading a book, and chaining together new commands to get a password is really rewarding. 

Once you finish bandit, they also have a lot of other wargames that you can branch into. Some of them focus more on cryptography, others switch to hacking web applications, and others continue in the command line. A lot of these wargames have been online for a while, so if you want to cheat, there are probably results out there that’ll show you the complete solution. I’d suggest not looking though, since the entire point is to learn!



![Bellingham Codes - Wargames (4).jpg](/squarespace_images/Bellingham+Codes+-+Wargames+%284%29.jpg)
  


  



Microcorruption (
[https://microcorruption.com](https://microcorruption.com)) is entirely in-browser, so this is a great one to try if you don’t want to do the initial setup that I talked about earlier. Microcorruption is a fun wargame with a storyline: You’re a thief who plants to break into warehouses to steal briefcases from a company, which are full of bearer bonds, worth millions of dollars. The warehouses have electronic locks, however, and you need to break them. With in-browser debugger, assembly, and a console, you’re tasked with reverse engineering what the code running on the electronic locks is doing, and then figuring out how to make the locks open.

Each level is in a new location around the world, and is harder than the last. The assembly you’re debugging through is a real assembly language, but not the one that’s probably running on your computer right now. The code is in MSP430 assembly, used by TI (the calculator company). If you’ve learned x86 assembly before, or really any assembly language before, it’ll be pretty easy to pick up. If you haven’t learned any assembly at all, Microcorruption has an intro PDF that gives you the basics needed. And since it’s a real assembly language and not made up for the puzzle, you can search online for more info if you need it.

They start with a basic puzzle and ramp up in difficulty pretty fast, but the puzzles are something you can figure out, and often don’t require complex concepts. For the most part you’re normally dealing with buffer overflows, and understanding the basics of how a computer works with registers and memory.

**Where to go from here**








  

    
  
    

![](/squarespace_images/image-asset.jpeg)
  

So maybe you’ve started poking around at sites, and completed some challenges. What do you do from there? Well there’s a couple options. First, there’s a website out there called wechall 
[https://www.wechall.net](https://www.wechall.net/), that collects stats and scores for individuals, across the different wargames sites. You can sign up there, and then collect how far you’ve gotten on overTheWire, Hack the box, and more.

If you’d like more of a challenge, and a time limit, you could start doing the CTFs I talked about earlier. These are normally timed to be a day or a weekend, and have new interesting challenges. CTFtime 
[https://ctftime.org](https://ctftime.org/) is a website that tracks up and coming CTFs, with links to the sites and info on requirements. Some CTFs will reward you with swag or even cash, and if you’re really good, you could potentially get to the defcon CTF and win entrance to defcon for free for life. If you do, remember who told you about CTFs, I may cash in on that later…

**Wrap up**

So there you have it, a brief overview of what wargames are, some examples, and resources to get started. Wargames are a great intro to hands-on security learning in a legal, relatively risk-free setup. They’re also just a lot of fun, and I’d suggest playing some even if you’re not really interested in security but you love a good puzzle and playing with computers. 

**Resources**

[https://picoctf.com](https://picoctf.com/) - CTF aimed at middle and high schoolers (also known as security beginners). Created by Carnegie Mellon, they also run the current year’s CTF year-round for others to play around on.

[https://overthewire.org/wargames](https://overthewire.org/wargames/) - Bandit wargame is linux, Natas is php websites, Leviathan is more linux, Krypton is cryptography. A wide array of challenges to choose from.

[https://microcorruption.com](https://microcorruption.com) - reverse engineering embedded systems, great fun. Give you a better understanding of how computers work at a low level, uses real assembly language, which is a plus.

[https://www.hackthebox.eu](https://www.hackthebox.eu) - Basically requires you have a VPN set up. There’s a rotating set of VMs that are vulnerable to hacking, so it gives new challenges all the time. Has both a free and “pro” version, free can give you a lot of learning opportunities.

[https://ctftime.org](https://ctftime.org)

[https://www.wechall.net](https://www.wechall.net)
