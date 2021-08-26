---
layout: post
title: Setting up ESP8266 with VSCode, Arduino, and Make
categories:
- technical write up
- side project
- How-to
tags:
- side project
- microcontrollers
- embedded
status: publish
type: post
published: true
excerpt_separator: <!--more-->
---

Continuing my exploration of embedded systems, I decided to try my hand at the ESP8266, a popular microcontroller. It's apparently being phased out and replaced with the ESP32, but it still has a lot of fuctionality, and perhaps more importantly, I already had one on a dev board laying around. 

Because I'm all about learning, and also about doing things the hard way, I decided to use a different toolchain setup than what Adafruit suggests (which is just using the arduino ecosystem). Instead, I'll go for something a little more complicated...

<!--more-->

## Plan
The plan is to use the ESP8266, in this case on the [adafruit feather Huzzah with ESP8266](https://www.adafruit.com/product/2821), with the Arduino libraries, but using VSCode instead of the Arduino IDE. In the spirit of KISS (Keep It Simple Stupid), I decided to use Make to glue everything together. Happily I didn't have to do this all from scratch, and mainly had to tweak things instead. Let's get into it.

## Benefits
Why am I even doing this in the first place? Well:

- **Arduino Libraries are easy to use** - I _could_ work on getting espressif's SDK for the ESP8266 going, and figure out how to flash the code onto the huzzah myself. But frankly, that's a bit too much reinventing the wheel right now. I want to get something functional, and the code I have already uses Arduino libraries and calls, so why re-write it all? Plus, getting more libraries is really easy with the Arduino IDE.
- **More Useful IDE** - this is very subjective, but frankly, I like VSCode a lot better than the Arduino IDE. I got a file explorer, a terminal, and a text editor with syntax highlighting, what more could a gal need? Its level of flexibility means I can do everything I want in it (including writing this blog post). I don't have to relearn a new IDE for embedded stuff, I can stick with what I know. Given all there is to know about embedded systems, I'm willing to skip the less interesting bits.
- **Testing** - I did googling but I couldn't find anything about doing unit tests in the Arduino IDE. I want to build more complex programs, which means testing. Debugging boneheaded errors because I _couldn't_ do unit tests seemed very silly. If I'm going to debug boneheaded errors, it's because I _decided_ not to do unit tests. And again, there's a lot for me to learn here, doing unit tests as I go will help me on my embedded systems adventure.
- **Flexibility** - If I want to have multiple builds, or add extra things to my build process, I can! I have to argue with make about it, but it's at least possible, and kind of already a given with the tools I'm using. 
- **Local** - I know there's a couple online embedded IDE's out there (Platformio comes to mind), but call me old-fashioned: I like to have code on my computer. Sure, I'll back it up (normally to github), but having a local copy, and not relying on an online cloud service, feels like one less thing to worry about. If my code breaks or disappears, it's because of me, not because a cloud service decided they wanted more money and paywalled me out of my code.

## The Software

### Arduino IDE
The arduino IDE is actually still needed for this setup. I know, I know, it seems silly to download something you don't plan on using. But it does provide easy access to arduino libraries, plus a nice serial monitor and plotter. I don't like coding in it, but those are nice features to have, so it's simpler to just download it and use the bits you care about. Download the software directly from Arduino on their [software download page](https://www.arduino.cc/en/software). Make sure to select the correct version, and don't get distracted by the web editor they're advertising. You want the downloadable version.

### VSCode
VSCode, aka Visual Studio Code, is made by Microsoft, and is completely different than their large and somewhat unwieldy Visual Studio IDE. Yes, Microsoft is still terrible at naming things. VSCode is actually open source, and free for private and commercial use. It also has a lot of plugins, built-in terminal, syntax highlighting, and is pretty lightweight for how useful it is. Think of it as somewhere between Sublime and Eclipse/Visual Studio IDE. It also runs on Mac, Linux, and Windows. You can download it from [Microsoft's  visual studio code website](https://code.visualstudio.com/)

### Makefile
Make is old-school (sorry if you're reading this and remember when it was new. But like, it's true. You're old-school now. It came out in '76!) It's a build automation tool that runs on the command line. You can make custom production, dev, test, whatever-else build processes. You can probably get it to clean your kitchen. The commands can be arcane and confusing, but it can do a little bit of everything if you learn the right incantation.
If you have linux, you probably already have it. 

### The others
I'm also using git, python, and g++. The pre-made makefile also calls some perl scripts. Just to give you a full understanding of what I'm using.

## The Set-up

First, make sure you have all of the above listed software. Make sure they all seem to work. Now lets start tweaking things.

### Arduino Libraries
Since you want to work on an ESP8266, first you'll have to download some libraries. The bare-minimum is the ESP8266 board library. This is from [https://github.com/esp8266/Arduino](https://github.com/esp8266/Arduino), and the install instructions are pretty straightforward. Add a new board manager URL, then download the ESP8266 board. 

To make sure it works, I'd suggest trying to flash one of the example sketches to the esp8266, make it blink or run a wifi scan.

### VSCode
I Installed a Microsoft-written plugin that helps with syntax: [https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools). The webpage shows the install instructions. Later there's some VSCode config files you can add to your project to make its error alerts more useful. 

### Makefile
There's actually two makefiles for this. The first is a pre-built one that came from [https://github.com/plerup/makeEspArduino](https://github.com/plerup/makeEspArduino). This has install instructions, and works! But it didn't support how I setup my project (see below), so I forked it and modified it. It's now available on my [github repo](https://github.com/dthurow/makeEspArduino) with the change I had to make. 

That's the first makefile, the second is a custom one that will live in your project. I'll explain more below.

## Project setup

Folder setup described below. -> means it's a directory, tabs indicate which files are in what folder (e.g. "unity" folder is inside the "test" folder).

```
->Project name
    ->.vscode
    ->build
    ->doc
    ->test
        ->unity
            unity_internals.h
            unity.c
            unity.h
    ->src
    ->inc
    ->makeEspArduino
    makefile
    readme.md
    .gitignore
    .gitmodules
```

I'll go through each of these folder and files to explain what's in them.

### makeEspArduino
This is actually a git submodule. This folder contains the [https://github.com/dthurow/makeEspArduino](https://github.com/dthurow/makeEspArduino) repo. It lets you keep all your code in one place. The `.gitmodules` file (explained below) automatically pulls that in when you do `git clone --recurse-submodules` on any project you make following this setup.

### .gitmodules
This lets you have git repos in folders inside other git repos. In this case, we're adding the [makeEspArduino](https://github.com/dthurow/makeEspArduino) into the project. The contents of this file are:

```
[submodule "makeEspArduino"]
	path = makeEspArduino
	url = git@github.com:Dthurow/makeEspArduino.git
```

### makefile
This file does two things: 
1. Sets the configuration variables that the `makeEspArduino` uses
1. Sets up the ability to run tests (I use the [unity framework](http://www.throwtheswitch.org/unity))

To make this work for you, you'll have to make sure that:
- the `LIBS` directories are where your arduino libraries are.
- The `SKETCH` variable is set to your main file (that contains your `setup()` and `loop()` functions)
- Have g++ downloaded
- Set the `BOARD` to the correct value. To figure out what it should be, you can run `make list_boards` and the `makeESPArduino` file will spit out a list of accepted boards. It also has a `generic` option if yours isn't on the list

{% highlight make %}
DIR := ${CURDIR}
SKETCH = $(DIR)/src/[YOUR MAIN FILE HERE]
BUILD_DIR = $(DIR)/build
BOARD = huzzah
LIBS = $(HOME)/.arduino15/packages/esp8266/hardware/esp8266/2.7.4/libraries $(HOME)/Arduino/libraries 
EXCLUDE_DIRS = test
include $(DIR)/makeEspArduino/makeEspArduino.mk

#everything below here is for setting up tests
TARGET_EXTENSION=.out
#Path Definitions
PATHU = test/unity/
PATHS = src/
PATHT = test/
PATHI = inc/
PATHB = build/

#determine our source files
SRCU = $(PATHU)unity.c
SRCS = $(wildcard $(PATHS)*.cpp)
SRCT = $(wildcard $(PATHT)*.cpp)
SRC = $(SRCU) $(SRCS) $(SRCT)

#Files We Are To Work With
OBJU = $(patsubst $(PATHU)%.c,$(PATHB)%.o,$(SRCU))
OBJS = $(patsubst $(PATHS)%.cpp,$(PATHB)%.o,$(SRCS))
OBJT = $(patsubst $(PATHT)%.cpp,$(PATHB)%.o,$(SRCT))
OBJ = $(OBJU) $(OBJS) $(OBJT)

#Other files we care about
DEP = $(PATHU)unity.h $(PATHU)unity_internals.h
TGT = $(PATHB)test$(TARGET_EXTENSION)

#Tool Definitions
CC=g++
CFLAGS=-I. -I$(PATHU) -I$(PATHI) -I$(PATHS) -DTEST

test: $(PATHB) $(TGT)
	echo "running tests"
	./$(TGT)

$(PATHB)%.o:: $(PATHS)%.cpp $(DEP)
	echo "source compiling"
	$(CC) -c $(CFLAGS) $< -o $@

$(PATHB)%.o:: $(PATHT)%.cpp $(DEP)
	echo "tests compiling"
	$(CC) -c $(CFLAGS) $< -o $@

$(PATHB)%.o:: $(PATHU)%.c $(DEP)
	echo "unity compiling"
	$(CC) -c $(CFLAGS) $< -o $@

$(TGT): $(OBJ)
	echo "linking"
	$(CC) -o $@ $^

.PHONY: test

{% endhighlight %}

### test
This folder is where you'll put your test files (e.g. `testMyCoolCode.cpp`). Your tests can use the unity framework, which you can find out more about here: [http://www.throwtheswitch.org/unity](http://www.throwtheswitch.org/unity). You only need the three files I list in the folder setup, and you can get the latest from github [https://github.com/ThrowTheSwitch/Unity/tree/master/src](https://github.com/ThrowTheSwitch/Unity/tree/master/src).

### .vscode
This folder stores VSCode-specific config files that override your default configs on a project-specific basis. The `makeEspArduino` makefile actually has a command that auto-creates this info for you. Once the makefile and your main source file are created, you can run `make vscode` and it will autogenerate your `.vscode` folder. In my case, though, to get VSCode's syntax checker to fully work, I had to update the `includePath` in the `c_cpp_properties.json` file. I updated mine to:
```
            "includePath": [
                "${env:HOME}/.arduino15/packages/esp8266/hardware/esp8266/2.7.4/tools/sdk/include",
                "${env:HOME}/.arduino15/packages/esp8266/hardware/esp8266/2.7.4/tools/sdk/lwip2/include",
                "${env:HOME}/.arduino15/packages/esp8266/hardware/esp8266/2.7.4/tools/sdk/libc/xtensa-lx106-elf/include",
                "${env:HOME}/.arduino15/packages/esp8266/hardware/esp8266/2.7.4/cores/esp8266",
                "${env:HOME}/.arduino15/packages/esp8266/hardware/esp8266/2.7.4/variants/generic",
                "${env:HOME}/.arduino15/packages/esp8266/hardware/esp8266/2.7.4/libraries/**",
                "${env:HOME}/Arduino/libraries/**",
                "${workspaceFolder}/build",
                "${workspaceFolder}/src"
                
            ],
```
And then VSCode no longer errored out on not seeing the Arduino Library folders. 


### .gitignore
This one's simple, just ignore the build folder and the special vscode folder:

```
build
.vscode
```

### src
Where your actual production code lives! I know, there's a lot of other _stuff_ this project has, but honest, it's all there for a good reason.

### inc
Honestly I'm on the fence if you really need this folder. This can be used to include needed header files. You can also just keep them in `src`, I won't tell.

### readme.md
A good file for any project, so you can write up setup or contribution info.

### build
This is where the makefiles will build out any intermediary files and where it'll put the file compiled version of the code. You can clear this folder out by typing `make clean`. Sometimes the default `make all` errors because of linker issues. In that case, run a `make clean` then `make all`.

### doc
A place to put any documentation you may have! You do keep written documentation, right? Because "self-documenting code" isn't actually a thing? Yeah of course you do, good job you.


# The Final Result

Hopefully, a working project! I've put together the template on github [https://github.com/Dthurow/generic-esp8266-project-with-vscode-and-arduino](https://github.com/Dthurow/generic-esp8266-project-with-vscode-and-arduino) that you can pull down if you want to do that instead of building it out manually. Please do pull requests or open issues with any updates you may have, I'm curious if this project will be useful for others, or if there's other ways of doing things I just don't know about.

Good luck and happy programming!