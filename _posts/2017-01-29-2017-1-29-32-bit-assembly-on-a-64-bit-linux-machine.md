---
layout: post
title: 32-bit Assembly on a 64-bit Linux machine
slug: 32-bit-assembly-on-a-64-bit-linux-machine
categories:
- How-to
- Assembly
tags:
- how-to
- assembly
- 32-bit vs 64-bit
status: publish
type: post
published: true
meta: {}
---

As part of my learning about low-level computing, I figured it would be best if I could learn more about assembly. The book 
Hacking: the Art of Exploitation (
[https://www.nostarch.com/hacking2.htm](https://www.nostarch.com/hacking2.htm)) has some beginner assembly stuff in it, so I decided I wanted to do some writing of assembly myself.

I quickly came upon a problem, however. All of the examples are in x86 assembly (aka 32-bit). My machine is running as x64 (aka 64-bit). This means compiling 32-bit code isn't as easy as copying the compile commands in the book (because that would be too easy). After some hunting around and trying out some GCC commands with different flags (that unfortunately all ended in tears),  I ended up using the same commands the book had to assemble and link it, just with some different flags to make it 32 and not 64. (as an aside, as noted in the title of this post, I'm running on Linux. I haven't tried any of this on a windows machine yet)

So let's say you've written the following assembly, a classic hello world bit, and saved it as HelloWorld.asm.

    BITS 32

    section .text
    global _start

    _start:
    mov eax, 4;system call number 4 is write
    mov ebx, 1;file descripter (std_out)
    mov ecx, msg ;my message
    mov edx, 13;length of my message
    int 0x80;call it

    ; syscall exit(0)
    mov eax, 1;system call number 1 is exit()
    mov ebx, 0;exit(0)
    int 0x80;call it

    section .data
    msg db "Hello, world!", 0

The book has you compile with nasm, which I didn't have, at first, so install with the normal apt-get command.

sudo apt-get install nasm

Now you can run the following two commands, and they'll give you an executable file called "HelloWorld" in your current directory.

    nasm -f elf HelloWorld.asm -o HelloWorld.o
    ld -m elf_i386 HelloWorld.o -o HelloWorld

Now remembering the flags and the fact that I have to run 
two whole commands every time I wanted to run my assembly was much too complicated and aggravating. So I spent a good 45 minutes or so whipping up a bash script that does the same thing with only one command. It was a solid refresher, since my most recently written shell script was in powershell. Copy the below bash script and save it as you like (I saved it as compile.sh)

    #!/bin/bash

    if [ $# -ne 1 ]; then
    echo $0 usage is: $0 \<filename\>
    echo "filename must end in a .asm"
    exit 1
    fi
    #get the filename in a nicer named variable
    fileName=$1

    #get last 4 characters of filename to make sure they match
    endChar=${fileName:$[${#fileName}-4]}

    if ["$endChar" = ".asm" ]; then
    #It takes the filename, and returns a substring 
    #starting from index 0, and pulls in the length 
    #of the filename -4 number of characters
    #to strip off the ".asm" at the end of the filename
    truncFileName=${fileName:0:$[${#fileName}-4]}

    nasm -f elf $fileName -o $truncFileName.o
    ld -m elf_i386 $truncFileName.o -o $truncFileName
    else
    echo "filename must end in .asm for this to work"
    exit 1
    fi;

Now make it so the file is executable, and voila, you're good to go.

    chmod +x ./compile.sh

All you have to do is do call ./compile.sh [filename] and you'll get an executable version of your assembly. The only downside right now is it requires the assembly file to be called [something].asm for it to work (so other file extensions aren't allowed), but still. I'm planning on doing .asm because that seems like a standard for assembly files, so it shouldn't be a problem.

## Online References


### Assembly


* Basics of using nasm - 
[http://ccm.net/faq/1559-compiling-an-assembly-program-with-nasm](http://ccm.net/faq/1559-compiling-an-assembly-program-with-nasm)


* 64-bit assembly fun - 
[https://thebrownnotebook.wordpress.com/2009/10/27/native-64-bit-hello-world-with-nasm-on-freebsd/](https://thebrownnotebook.wordpress.com/2009/10/27/native-64-bit-hello-world-with-nasm-on-freebsd/)


* Stack overflow, because of course they have an answer - 
[http://stackoverflow.com/questions/18429901/compiling-32-bit-assembly-on-64bit-system-ubuntu#18430354](http://stackoverflow.com/questions/18429901/compiling-32-bit-assembly-on-64bit-system-ubuntu#18430354)

### Bash


* Nice bash reference - 
[http://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO.html](http://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO.html)
