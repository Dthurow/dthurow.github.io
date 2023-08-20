---
layout: post
title: Programming an ATtiny85
categories:
- technical write up
- side project
- How-to
tags:
- side project  
- microcontroller
- programming ATTiny85
- embedded
status: publish
type: post
published: false
excerpt_separator: <!--more-->
toc: true
---

# Current TODOs
- make this article more coherent
- get pictures of current wiring and setup

### Intro
Using the knowledge I gained from my [previous post]({%post_url 2021-05-25-directly-programming-an-atmega328p-from-an-arduino-uno %}), I decided I wanted to scale down. The ATmega328p from the Uno is great, but for really simple projects (*cough* [mindfulness bracelet]({%post_url 2021-07-28-adafruit-mindfulness-bracelet %}) *cough*), it would be total overkill. Enter the ATtiny85. A member of the AVR family, this lil' guy is an 8-bit AVR RISC-based microcontroller. It has fewer bells and whistles, but for a relatively simple setup like the mindfulness bracelet, it should have more than enough oomph. 


But before I get ahead of myself, I need to be able to actually program an ATtiny85. Which leads me to...
<!--more-->
### The Plan

1. Wire up a simple LED and button circuit for the ATtiny85.
1. Use Arduino IDE to create a simple blinky program
1. Send the compiled blinky to the ATtiny85, using an Arduino Uno as an ISP.
1. See if I can use interrupts in Arduino ecosystem by adding a button to toggle the light either on or off


## Steps


### wire up a breadboard

| **color** | **arduino** | **ATtiny85** |
| red | 3.3v | pin 8 - VCC |
| black | 10 | pin 1 - reset |
| grey | GND | pin 4 - GND |
| purple | 13 - SCK | pin 7 - SCK |
| yellow | 12 - MISO | pin 6 - MISO |
| green | 11 - MOSI | pin 5 - MOSI |

And to actually test if my blink program works, two orange wires, one from ground to the negative of an LED, one from the positive side of an LED to physical pin 3, which corresponds with PB4.

When researching how to set this up, I came across [http://highlowtech.org/?p=1706](http://highlowtech.org/?p=1706), which says you should add a 10μF capacitor between arduino uno's reset and gnd pin (negative to gnd). However, that didn't seem to affect my ability to upload my programs, so I left that out. 

### Creating the sketch and uploading

To use the ATtiny85 with the arduino IDE, I needed to add an attiny library to list of arduino IDE board managers: https://raw.githubusercontent.com/damellis/attiny/ide-1.6.x-boards-manager/package_damellis_attiny_index.json
Once that's added, I can add the attiny package in the board manager. 

To actually send the sketch over to the attiny, make sure your configuration under the "Tools" in Arduino IDE match below.

|board | Attiny 25/45/85|
|processor | attiny85|
|clock | internal 1mhz |
|port | your port (my case, COM3) |
|programmer | arduino as ISP |

I stole the basic arduino blinky sketch and tweaked it just a bit. Since I had connected my LED to the physical pin 3 on the attiny85, which corresponds to PB4, I set the test pin to 4 in the sketch.
```
#define TESTPIN 4
// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(TESTPIN, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(TESTPIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(TESTPIN, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);                       // wait for a second
}
```
Since I'm using the arduino uno as an ISP,  upload it to the ATtiny85 by doing Sketch-> Upload using Programmer.

NOTE: I decided to play with Wowki, and created a sketch version of this here: [https://wokwi.com/projects/373599051955989505](https://wokwi.com/projects/373599051955989505)


### Adding Interrupts

Since attiny is an AVR microcontroller, I can use the AVR libraries, including the interrupt and sleep!

I added a button connected to physical pin 2 (aka PCINT3/PB3), and ground.

Next step was seeing if I could use interrupts with Arduino, created a test setup in wowki here: [https://wokwi.com/projects/373599069478744065](https://wokwi.com/projects/373599069478744065)

sketch code is:

```
#include <avr/interrupt.h>
#include <avr/sleep.h>

#define LED_PIN 4
#define BUTTON_PIN 3

bool lightOn = true;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_PIN, OUTPUT);
  // initialize the button pin as an input that's a pullup
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  //set interrupts to trigger on the rising edge
  MCUCR |= 0b00000011;

}

ISR(PCINT0_vect) {
  GIMSK &= ~0b00100000;  // Turn off general pin change interrupts
  sleep_disable();
}

void sleep() {
  sleep_enable();
  noInterrupts(); //disable interrupts globally
  GIMSK |= 0b00100000;  // Turn on general pin change interrupts 
  PCMSK |= (1 << BUTTON_PIN); //set the specific pin to trigger on
  interrupts(); //enable interrupts globally
  sleep_cpu();
}

/**
    Waits until the user pressed the button, and returns the index of that button
*/
byte readButton() {
  while(true) {
      if (digitalRead(BUTTON_PIN) == LOW) {
        return BUTTON_PIN;
      }
    
    sleep();
  }
}

// the loop function runs over and over again forever
void loop() {

  if (lightOn)
  {
    digitalWrite(LED_PIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  }
  else
  {
    digitalWrite(LED_PIN, LOW);    // turn the LED off by making the voltage LOW
  }

  //wait on a button press
  readButton();
   // Wait until button is released.
  while (digitalRead(BUTTON_PIN) == LOW);
  delay(150); //delay to avoid bounces
  //only reach here if button was pressed, so toggle value
  lightOn = !lightOn;

}
```


### Troubleshooting
While working on this, I got an "avrdude: Yikes!  Invalid device signature." when I tried to upload the program using the programmer. I've previously had that, and it was related to an incorrect baudrate. However, this time, it was on me, I didn't have reset pin (physical pin 1) connected to arduino 10!


If you get an error about how the ID for attiny isn't correct, make sure you set it to attiny85 in the "processor" field in the tools section

Confirmed: pin numbers in arduino IDE correspond with PBx numbers on pinout (e.g. PB3 is physical pin 2, referenced in arduino ide as 3)

## Overview of ATtiny85 functionality
### Pinout info

![pinout](/assets/using-attyiny85/Chip-Pinout.png)

**Port B** is a 6-bit bi-directional I/O port with internal pull-up resistors (selected for each bit)

**Reset input**. A low level on this pin for longer than the minimum pulse length will generate a reset


The **Status Register** contains information about the result of the most recently executed arithmetic instruction. This
information can be used for altering program flow in order to perform conditional operations. Note that the Status
Register is updated after all ALU operations, as specified in the Instruction Set Reference. This will in many cases
remove the need for using the dedicated compare instructions, resulting in faster and more compact code.
The Status Register is not automatically stored when entering an interrupt routine and restored when returning
from an interrupt. This must be handled by software.

### Clock

![clock source options](/assets/using-attyiny85/ClockSource.png)

The device is shipped with CKSEL = “0010” (Calibrated internal oscillator), SUT = “10” (start up time assumes slowly rising power), and CKDIV8 programmed. The default clock source setting is therefore the Internal RC Oscillator running at 8 MHz with longest start-up time and an initial system clock prescaling of 8, resulting in 1.0 MHz system clock. This default setting ensures that all users can make their
desired clock source setting using an In-System or High-voltage Programmer.

If CKDIV8 is programmed, CLKPS bits are reset to “0011”, giving a division factor of eight at
start up.

### Power Savings

Idle mode enables the MCU to wake up from external triggered interrupts as well as internal ones like the Timer
Overflow

The MCU Control Register contains control bits for power management.

to set the desired sleep mode using set_sleep_mode() , and then call sleep_mode(). This macro
automatically sets the sleep enable bit, goes to sleep, and clears the sleep enable bit.

### Interrupts
The External Interrupts are triggered by the INT0 pin or any of the PCINT\[5:0] pins. Observe that, if enabled, the interrupts will trigger even if the INT0 or PCINT\[5:0] pins are configured as outputs. 

The INT0 interrupts can be triggered by a falling or rising edge or a low level. This is set up as indicated in the specification for the MCU Control Register – MCUCR.

When the AVR exits from an interrupt, it will always return to the main program and execute one more instruction before any pending interrupt is served.

The interrupt execution response for all the enabled AVR interrupts is four clock cycles minimum

If an interrupt occurs when the MCU is in sleep mode, the interrupt execution response time is increased by four clock cycles. 

AVR GCC uses the ISR macro to define an ISR. This macro requires the header file: <avr/interrupt.h>. In AVR GCC an ISR is defined as follows:
```
#include <avr/interrupt.h>
ISR(PCINT1_vect)
{
 //code
}
```
to disable global interrupts use `cli()` 
to enable, use `sei()`

### I/O Pins
Three I/O memory address locations are allocated for each port, one each for the Data Register – PORTx, Data
Direction Register – DDRx, and the Port Input Pins – PINx

 optional internal pull-ups.

 there's a summary at: 23. Register Summary which gives address

 ### Compiling

potential makefile? [https://gist.github.com/edwardhotchkiss/9378977](https://gist.github.com/edwardhotchkiss/9378977)

Potential commands?:
```
avr-gcc -Wall -Os -mmcu=attiny85 main.c
avr-objcopy -O ihex -j.text -j.data a.out main.hex
```


From my programming an atmega328p:
```
    avr-gcc -mmcu=atmega328p blink.c
    avr-objcopy -O ihex -j.text -j.data a.out a-small.hex
    avrdude -v -c /etc/avrdude.conf -p atmega328p -c stk500v1 -P /dev/ttyUSB0 -b 19200 -U flash:w:a-small.hex:i
```

### Sending data to ATtiny85

I know I have to use an arduino as an ISP, but what do I connect it to?
The programming process uses VCC, GND and four data pins. Three pins connect MISO, MOSI and SCK between the programming micro and the target micro, the fourth pin from the programming micro goes to the reset pin of the target.
  
### Resources


Datasheet is here: [https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-2586-AVR-8-bit-Microcontroller-ATtiny25-ATtiny45-ATtiny85_Datasheet.pdf](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-2586-AVR-8-bit-Microcontroller-ATtiny25-ATtiny45-ATtiny85_Datasheet.pdf)


AVR programming info here: [https://ww1.microchip.com/downloads/en/Appnotes/Atmel-42787-AVR-Software-User-Guide_ApplicationNote_AVR42787.pdf](https://ww1.microchip.com/downloads/en/Appnotes/Atmel-42787-AVR-Software-User-Guide_ApplicationNote_AVR42787.pdf)

avr-libc is an open source development toolchain for AVR: [https://www.nongnu.org/avr-libc/user-manual/overview.html](https://www.nongnu.org/avr-libc/user-manual/overview.html)

Arduino as ISP: [https://docs.arduino.cc/built-in-examples/arduino-isp/ArduinoISP](https://docs.arduino.cc/built-in-examples/arduino-isp/ArduinoISP)