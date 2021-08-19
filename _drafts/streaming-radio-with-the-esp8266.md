

Installed libraries listed here: https://learn.adafruit.com/adabox004/arduino-ide-and-installing-new-libraries

Followed set up here: https://github.com/plerup/makeEspArduino

running `make -f makeEspArduino.mk DEMO=1 flash` defaulted to a wifi scanning script, could look at it on serial monitor or `screen /dev/ttyUSB0 115200` (`ctrl+a` followed by `k` will kill a screen session)


use command `make -f makeEspArduino.mk install` to add `espmake` command to terminal


copied the internet-streaming.ino file into a separate folder:

danielle@danielle-z-series:~/Documents/CProjects/StreamingRadio/src$ espmake
Esp-version.cpp
spiffs_api.cpp
cdecode.cpp
/bin/sh: 1: /bin/xtensa-lx106-elf-g++: not found
/bin/sh: 1: /bin/sh: 1: /bin/xtensa-lx106-elf-g++: not found
/bin/xtensa-lx106-elf-g++: not found
/home/danielle/makeEspArduino/makeEspArduino.mk:265: recipe for target '/tmp/mkESP/internet_streaming_generic/spiffs_api.cpp.o' failed
make: *** [/tmp/mkESP/internet_streaming_generic/spiffs_api.cpp.o] Error 127
make: *** Waiting for unfinished jobs....
/home/danielle/makeEspArduino/makeEspArduino.mk:265: recipe for target '/tmp/mkESP/internet_streaming_generic/cdecode.cpp.o' failed
make: *** [/tmp/mkESP/internet_streaming_generic/cdecode.cpp.o] Error 127
cencode.cpp
/bin/sh: 1: /bin/xtensa-lx106-elf-g++: not found
/home/danielle/makeEspArduino/makeEspArduino.mk:265: recipe for target '/tmp/mkESP/internet_streaming_generic/cencode.cpp.o' failed
make: *** [/tmp/mkESP/internet_streaming_generic/cencode.cpp.o] Error 127
/home/danielle/makeEspArduino/makeEspArduino.mk:265: recipe for target '/tmp/mkESP/internet_streaming_generic/Esp-version.cpp.o' failed
make: *** [/tmp/mkESP/internet_streaming_generic/Esp-version.cpp.o] Error 127


Turned off computer and restarted

added make file to my set up:
    DIR := ${CURDIR}
    SKETCH = $(DIR)/src/internet_streaming.ino
    BUILD_DIR = $(DIR)/build

    include $(HOME)/makeEspArduino/makeEspArduino.mk

now seems to work. 

Once added the makefile, it would flash, but the new code wouldn't run. had to update the makefile to set the board to huzzah:

    DIR := ${CURDIR}
    SKETCH = $(DIR)/src/internet_streaming.ino
    BUILD_DIR = $(DIR)/build
    BOARD = huzzah
    include $(HOME)/makeEspArduino/makeEspArduino.mk

Now can run blink!

Changed code to the adafruit internet streaming radio sketch, VScode complains
did `make vscode` to make vscode config stuff. Ended up having to add two extra lines to the generated `c_cpp_properties.json` file. Added to includePaths section:

                "${env:HOME}/.arduino15/packages/esp8266/hardware/esp8266/2.7.4/libraries/**",
                "${env:HOME}/Arduino/libraries/**",

So that VScode intellisense would find the header files included in the internet streaming radio code.

Ran `make`, and it errored without finding the libraries. added them by adding below line in makefile:

    LIBS = $(HOME)/.arduino15/packages/esp8266/hardware/esp8266/2.7.4/libraries $(HOME)/Arduino/libraries

make file now works!! :D


Made heirarchy diagram to figure out pieces

worked on sound output interface, an interface overtop the adafruit vs1053 library, so I can make a test version of the sound output during testing. 

implemented sound output interface and replaced references to adafruit library with soundOutput

c++ learnings:
- if you create an interface with only virtual functions, need to define the functions in your child class out-of-line (so use the :: syntax), so the GCC compiler builds out the vtable (mapping of virtual functions), correctly.
- to make sure headers aren't included multiple times, always do this trick in the .h files:
    #ifndef HEADERNAME_h
    #define HEADERNAME_h
    //header info goes here
    #endif


When building streamselector code and using it, getting this error:

    Exception (28):
    epc1=0x40203150 epc2=0x00000000 epc3=0x00000000 excvaddr=0x00000004 depc=0x00000000

    >>>stack>>>

    ctx: cont
    sp: 3ffffde0 end: 3fffffc0 offset: 0190
    3fffff70:  3ffee758 00000000 3ffee758 40203150  
    3fffff80:  3fffdad0 3ffee6b0 3ffee6ac 40202401  
    3fffff90:  3fffdad0 3ffef874 3ffee758 3ffee5e8  
    3fffffa0:  3fffdad0 00000000 3ffee5a8 402011f8  
    3fffffb0:  feefeffe feefeffe 3ffe8538 401002d1  
    <<<stack<<<

According to https://arduino-esp8266.readthedocs.io/en/latest/exception_causes.html this is from:

|28|LoadProhibitedCause|A load referenced a page mapped with an attribute that does not permit loads|

Not helpful -_-

Found: https://github.com/me-no-dev/EspExceptionDecoder Followed install

when I try to open it, it asks for ELF file. This link: https://github.com/me-no-dev/EspExceptionDecoder/issues/50 says it's looking for the compiled binary. 

Find it in: /home/danielle/Documents/CProjects/StreamingRadio/build/internet_streaming.elf

copy over stack from exception:

    >>>stack>>>

    ctx: cont
    sp: 3ffffde0 end: 3fffffc0 offset: 0190
    3fffff70:  3ffee758 00000000 3ffee758 40203150  
    3fffff80:  3fffdad0 3ffee6b0 3ffee6ac 40202401  
    3fffff90:  3fffdad0 3ffef874 3ffee758 3ffee5e8  
    3fffffa0:  3fffdad0 00000000 3ffee5a8 402011f8  
    3fffffb0:  feefeffe feefeffe 3ffe8538 401002d1  
    <<<stack<<<

Get result:

0x40203150: StreamSelector::PlayCurrentStream() at /home/danielle/Documents/CProjects/StreamingRadio/src/StreamSelector.cpp line 50
0x40202401: loop() at /home/danielle/Documents/CProjects/StreamingRadio/build/internet_streaming.cpp.cpp line 90
0x402011f8: loop_wrapper() at /home/danielle/.arduino15/packages/esp8266/hardware/esp8266/2.7.4/cores/esp8266/core_esp8266_main.cpp line 197


Maybe an issue with using the `new` keyword? https://arduino.stackexchange.com/questions/77061/why-is-it-considered-bad-practice-to-use-the-new-keyword-in-arduino 

**ERROR SOLUTION** I was redclaring streamselector variable inside the setup() function, so the setup I did didn't make it to the global streamselector. d'oh!

**NOTE** when using the `makeESPArduino` makefile, sometimes have to do `make clean` then `make` if you get linker errors. 

**WIFI fun**
somehow it stores the last access point in memory, so once it connects, you can delete your SSID and password from the code, reflash, and it still connects to the wifi???

https://www.arduino.cc/en/Reference/WiFi

**SD card limitations** 
according to docs https://www.arduino.cc/en/Reference/SDCardNotes

    You must use the 8.3 format, so that file names look like “NAME001.EXT”, where “NAME001” is an 8 character or fewer string, and “EXT” is a 3 character extension. People commonly use the extensions .TXT and .LOG. It is possible to have a shorter file name (for example, mydata.txt, or time.log), but you cannot use longer file names.

According to wikipedia:
    8.3 filenames are limited to at most eight characters (after any directory specifier), followed optionally by a filename extension consisting of a period . and at most three further characters. For systems that only support 8.3 filenames, excess characters are ignored. If a file name has no extension, a trailing . has no significance (that is, myfile and myfile. are equivalent). Furthermore, file and directory names are uppercase in this system, even though systems that use the 8.3 standard are usually case-insensitive (making CamelCap.tpu equivalent to the name CAMELCAP.TPU). However, on non-8.3 operating systems (such as almost any modern operating system) accessing 8.3 file systems (including DOS-formatted diskettes, but also including some modern memory cards and networked file systems), the underlying system may alter filenames internally to preserve case and avoid truncating letters in the names, for example in the case of VFAT.
