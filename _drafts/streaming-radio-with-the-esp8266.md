

Installed libraries listed here: https://learn.adafruit.com/adabox004/arduino-ide-and-installing-new-libraries

Followed set up here: https://github.com/plerup/makeEspArduino

running `make -f makeEspArduino.mk DEMO=1 flash` defaulted to a wifi scanning script, could look at it on serial monitor or `screen /dev/ttyUSB0 115200`


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