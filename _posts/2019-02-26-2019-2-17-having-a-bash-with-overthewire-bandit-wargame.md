---
layout: post
title: Having a Bash - With OverTheWire Bandit Wargame
slug: having-a-bash-with-overthewire-bandit-wargame
categories:
- CTF writeup
tags:
- ctf
- over the wire
status: publish
type: post
published: true
meta: {}
---

On the 25th I had some time off planned, and so decided to brush up on my bash skills using the wargame Bandit from OverTheWire (
[http://overthewire.org](http://overthewire.org)). They request you don’t do a write up for the solutions to the problems, so I wont. However, they do connect with a site called WeChall that lets you track what solutions you’ve solved. I created a profile there and linked it to track my progress. Here’s the link if you’re curious: 
[https://www.wechall.net/profile/qerolt](https://www.wechall.net/profile/qerolt).

As part of playing this wargame, I did brush up on some old knowledge and got some new knowledge about bash, so I thought I’d share some of the specifics that I’d discovered. Since there are multiple ways to solve most of these challenges, and they give suggestions of bash commands to look into for each challenge, I figure this isn’t going to be giving away any state secrets.



I’ve also done this wargame before, but didn’t store any info or have any proof of it, so I figured it made sense to try again, this time with better notes. I’ve gotten up to level 24 so far, though when I post this, I may have gotten farther. Check out the WeChall profile page if you’re curious.



# Background on the Bandit Wargame


OverTheWire has a collection of “wargames”, long running sets of puzzles that are, in their own words:

>Can help you to learn and practice security concepts in the form of fun-filled games.




Each set has a specific name, and have a specific set of security concepts they’re designed to teach. The one I worked on was “Bandit”, which in their own words again:

>The Bandit wargame is aimed at absolute beginners. It will teach the basics needed to be able to play other wargames




Which means a wide variety of bash commands that will be used in other wargames (I assume. I haven’t gotten to them yet). The basic setup is simple: you remote into a computer using ssh and a specified username, which has the current level’s number on it (e.g. bandit1 is for level 1). For each username, you have a password, and your goal is to get the password for the next username (so you’re logged in as bandit1, and trying to get the password for bandit2). OverTheWire has a set of hints for how to get the next password, as well as some bash commands that may prove helpful for this particular level. A lot of the time they give you more commands than you strictly need, but they’re all useful commands, so researching them isn’t going to hurt anyone. I’ve collected some of the ones that I used, and added some comments and opinions about what I discovered about them while trying to solve these puzzles.



# Bash commands - my opinions


## The bare-bones (aka dealing with the file system)


cd, pwd, ls, mkdir, rm, rmdir, touch, cat, nano

A lot of these commands are pretty standard, and the first ones that you’ll learn on any “command line intro” sort of articles/classes. One thing to note, though, is nano. It’s my personal go-to for doing simple text editing in a console, far and away above vim or emacs. As the joke goes, emacs is a great operating system but a terrible text editor. And figuring out how to exit vim can be a puzzle level for a wargame all by itself sometimes. Nano has all the commands you need to know displayed at the bottom of the screen. You don’t have to switch into writing mode, don’t have to memorize hotkey combos. You open a file, edit it, save it, and exit. Gotta love simplicity.



## Slightly more interesting


file, find, grep



File

File is actually a command I haven’t used all that much. It identifies the file type of a given file. Since I spend most my time in the Windows world, I’m used to always giving a file extension that denotes the type. Definitely nifty, and I’m curious to take a look at some more info on how it does that. I assume it determines type by looking at the beginning of the file stored on disk and comparing it with the different file types it knows of, but it may be more clever than that.



Find

Find is something I haven’t used too much either. Looking through the man page, I had some “reading grep’s man page” flashbacks. It has a lot of bells and whistles that I imagine are useful to lots of people, but as a noob it’s a bit much to take in all at once. I also discovered it doesn’t actually read the correct size of files, which, I have to say, is a bit aggravating, since it has a filter for size. Hunting for helpful info in the man page for this got me back into using grep to hunt through man pages though, so it’s not all bad (more on how I do that later).



Grep

Grep is one of those that I know I’m using the bare minimum of its abilities, but I’m okay with that. I feel kind of like I bought  a several thousand dollar gaming PC to play solitaire. It certainly works for that, but I’m not exactly stretching its abilities. I’ve just about got the ability to find a literal string in a given input, and can display the context around the found string, but that’s it.

## Not commands


Pipes

Ah, let me speak for my love of pipes. Being able to connect a string of bash commands together into a single line and get the exact result I want is just lovely. And I can’t help but feel very hacker-y when I do a series of pipes all at once.  However, it’s not all fun and games. I’ve been working with powershell a lot for work, and I’ll admit I quite like Window’s setup, where each command returns an object or set of objects that you can pipe into another command. This lets you reference properties from results using a “.”, and as a programmer that feels very natural. E.g. you can use the following command  to access the full path of each found file, along with a lot of other properties for each file:

    ls | foreach-object{echo $_.FullName}

Some of the bash commands output results that don’t pipe into other commands as easily as you’d think. Which causes a lot of aggravation when trying to build out a piped line of bash. I’ve been told it builds character, though, so I suppose I’ll just have to deal with it for now.

# Bash commands - to help you learn other bash commands


man, grep, whatis, less



Whatis

Whatis is a useful command when you come across a bash command you’ve never heard of before. You don’t want the life story of the command, you want to know what it does! Whatis gives a single line explanation for a particular command. E.g.

    whatis find

Returns:

    find (1)             - search for files in a directory hierarchy

Simple and to the point. A good starting  place before you jump into the more complicated commands, like man.

If you’ve done anything ever with bash, and innocently asked a question on the internet about it, you most likely got at least one reply that, in the sanitized form, told you: “Please read the man page for that command”. However, don’t take that personally, or resent the man command for it. It actually 
is useful, but, reading through big man pages to find what you want can be an art in and of itself, so don’t be discouraged if it seems too hard at first.

My personal recommendation for the man page: Read the intro paragraph, then skim the possible flags and look for examples. Most of the time, you’re looking for something specific. But you don’t want to jump to passing in thirty flags and doing pipes and redirects. Test the command bare-bones, get a handle on the basic flags that are needed to run, and go from there.



I also highly recommend a simple way of finding specific functionality in the man page: using a pipe with grep and context! For example: If you want to find an executable that you know is in a directory, but don’t remember the name. You’ve heard the find command is useful, but the man page is huge. Using the below command, you can search the man page for the word “exec”:



    man find | grep exec



That can give you the places in the man page that reference that word, and helps you find potential flags to use. Sometimes, however, you find a result, and want to read more, but grep only displays the line that has that word. In this case, you use the -C flag (capitalization is important). Using it lets you specify how many lines around the found word you want to display. So to display the 5 lines before and after the found word “exec”, use this command:



    man find | grep exec -C 5



And last but not least (or last but not less): You might be searching for a word in the man page that is really common, so it comes up with a bunch of results. You don’t want to have to scroll way back up after you run the man/grep command to get to the beginning of the found results. That’s where less comes into play. Pipe the results of the grep into less, and it’ll display a single page of text. If you want to see more of the results, you can press the down arrow to see more of the results. And if you’re done looking at the results, you can press Q to exit. Example command:



    man find | grep exec -C 5 | less



So the steps for learning about a new bash command are:

* Use whatis to get a one-line description


* Skim the man page


* Try to run the command with the bare bones version to understand how it works, re-read the man page if you run into issues


* Pipe the man page into grep and hunt for specific words for the thing you want to do with the command, potentially using less if there are a lot of results

# Resources for your own bash journey:


Of course, if you’re a hands-on learner, I’d recommend the Bandit wargame itself: 
[http://overthewire.org/wargames/bandit/](http://overthewire.org/wargames/bandit/)

It 
does sell itself as a hacker website though, so you should take some proper steps. I.e. using a VPN and/or a virtual machine that you can wipe after you connect and work on things.

Codeacademy has a lot of decent hands-on resources, even if they have started to move towards selling “pro” subscriptions. They have a glossary of command line commands, as well as a course for bash:

Glossary: 
[https://www.codecademy.com/articles/command-line-commands](https://www.codecademy.com/articles/command-line-commands)

Course: 
[https://www.codecademy.com/learn/learn-the-command-line](https://www.codecademy.com/learn/learn-the-command-line)



If you like reading, The Linux Command Line has a lot of it, explaining more in-depth about the command line. It also has the PDF version of the book “The Linux Command Line” from no starch press.

Online version: 
[http://www.linuxcommand.org/lc3_learning_the_shell.php](http://www.linuxcommand.org/lc3_learning_the_shell.php)

Link to PDF at: 
[http://www.linuxcommand.org/tlcl.php](http://www.linuxcommand.org/tlcl.php)
