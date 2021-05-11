---
layout: post
title: Microcorruption War Game (levels 1-8)
categories:
- CTF writeup
- Assembly
tags:
- microcorruption
- war game
- ctf
- assembly
status: publish
type: post
published: true
meta: {}
---

Microcorruption ([https://microcorruption.com/](https://microcorruption.com/)) is a long-time running “game” that gives you a series of puzzles that you have to solve. The fun bit? You solve the puzzles by learning and abusing assembly language! It uses MSP430 assembly (apparently an assembly language made by TI, the calculator guys), and is all in-browser. It displays the disassembled code, a live dump of memory, a console, and the register values. The story around it is simple: you’re trying to break into warehouses that are locked with an electronic lock. The company you work for has gotten the code that the locks use and disassembled it, and it’s your job to step through the code and figure out the password to get the lock to open. Each level uses a more and more complicated version of the electronic lock, but thankfully, the developers who made the lock code are pretty characteristically overworked and/or underpaid, so the code is rife with lovely bugs or just stupid programming that you can take advantage of.

             
          
![Screenshot of Microcorruption screen](/squarespace_images/Screenshot+of+Microcorruption+screen)


 

I haven’t gotten through the whole game yet by a longshot, but I’ve gotten a fair few, and wanted to walk you through some of the solutions.

But I’m not just going to give away the secret! Instead, for each level, I’ll give a list of hints that could potentially help you along the way. I'm not including the solutions, cuz cheating is only fun if you’re doing it in a really clever way ;)

 

## New Orleans


The first level after the tutorial! Really, it’s making sure you understand what the heck the disassembler window is actually displaying.

### Hints
* Put in a test password, then step through the code. Look to see if/where it compares your test password with another value. Can you see what the comparison is?
* Always look for helpful function names. Anything along the lines of “validate_password()” or “is_password_correct()”?



 

## Sydney


The wise-guys that made the lock pushed out a patch so the password wasn’t just sitting in memory, the jerks…

### Hints
* Put in a test password, then step through the code. Look to see if/where it compares your test password with another value. Can you see what the comparison is?
* This is looking awfully similar to the New Orleans, but the check_password isn’t looking in memory, it’s looking at something else...



## Hanoi


This one is finally different from the first two, and the developers had the gall to change the method names.

 

### Hints
* Put in a test password, then step through the code. Look to see if/where it compares your test password with another value. Where’s the comparison that splits the code flow between the “access granted” and “denied” logic?
* Line number 455a has the compare between what’s at 2410 and a hardcoded value cmp.b #0x3c, &Amp;0x2410 Is there a way you can write to that location and set it to 3c?



## Reykjavik


A big departure from the other ones. Just reading the disassembly and trying to logic through it isn’t going to be enough, you gotta step through and go slow (and probably having a scratchpad out too)

 

### Hints
* Put in a test password, then step through the code. Look to see if/where it compares your test password with another value. Where’s the comparison that splits the code flow between the “access granted” and “denied” logic? (Since some code gets shoved into memory and is executed there, you can’t use the disassembler to read the assembly. Make use of the assembler (https://microcorruption.com/assembler) or pay attention to the “Current Instruction” window so you can get what is actually happening in memory



## Cusco


They've made it tougher this time. Now the logic to validate the password isn't even stored on the device, instead it sends it over to a completely different module and just gets back a yes/no for if it's the right password. Looks like we're gonna have to stop guessing passwords and attack this in a different way....

### Hints
* The password prompt says “Remember: passwords are between 8 and 16 characters”. Is that really true?
* Where is it writing the password to? Any chance of stack overflows?



## Johannesburg


The popup says the developers have well and truly fixed issues with too long passwords, and it's still sending the password out, so we can't crack the password.

### Hints
* Put in a test password, then step through the code. Where is the password stored, and how does it make sure it isn't too long?
* It's comparing something on the stack with a hardcoded value. Can you just set that location to match the hardcoded value and trick the code?



## Whitehorse


Now we can't even call the unlock_door() function that triggers the unlock, so we can't just try to change the stack pointer.

### Hints
* You can't guess the password, and you can't call the unlock_door(). If only you could add some extra code in there to call that interrupt. Can you still control the pc, at least?
* Maybe this time you don't need to use filler before you take over the pc?



## Montevideo


This seems to be the sibling of the Whitehorse problem.

### Hints
* Step through the code. Looks like it's pretty similar to last time. Maybe you can use the same solution? Why or why not?
* If you can't do null bytes, that means you'll have to change your code, maybe use a different instruction?
