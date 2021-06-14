---
layout: post
title: Getting started with STM32 black pill - Getting blinky
categories:
- technical write up
- side project
- How-to
tags:
- side project
- microcontrollers
status: publish
type: post
published: true
---
Now that I've dipped my toes into the microcontroller world, lets cannonball in with the world of STM32 microcontrollers. There's a _ton_ of different microcontrollers that are all STM32, but I'll be starting with a relatively easy starting microcontroller. It's easy because it comes on a cheap development board. I'm talking about the We Act Studio's STM32F411 dev board, nicknamed the "Black Pill". The company that makes STM32 microcontrollers is called STMicroelectronics (Though later in this post I'll just refer to them as ST)and they have developed a lot of software and support for the STM32, so hopefully, it'll be a pretty easy process to ge the toolchain set up.


Going back to the Embedded For Everyone wiki [https://github.com/nathancharlesjones/Embedded-for-Everyone/wiki/1.-Getting-to-%22Blinky%22-with-a-new-MCU](https://github.com/nathancharlesjones/Embedded-for-Everyone/wiki/1.-Getting-to-%22Blinky%22-with-a-new-MCU), there's a nice graphic that shows all parts of an embedded system toolchain. AKA all the bits needed to actually program and debug a microcontroller. I annotated it with what I'm going to use, to give kind of an overview of my whole toolchain.

![Drawing representing the embedded toolchain. It is a simplified, visual version of the list below this image.](/assets/getting-started-with-stm32-black-pill-getting-blinky/Embedded-toolchain-full.png)

Lets go a little more in-depth about these pieces. 

1. **The MCU** - this is the STM32F411 microcontroller that is on the Black pill board
1. **Serial Wire Debug (SWD)** - I'll talk to it via the SWD header that's on the Black pill board
1. **Debug adaptor** - this is the ST-link v2. It connects to the SWD header on the black pill, and has a USB plug to let it talk to the computer. Everything after this in this list is software. The only bits of hardware needed are the Black pill and this ST-link v2!
1. **The IDE**- this contains all the software and packages I need to talk to the black pill. I'll be using the STM32Cube IDE. It contains the following sub-systems
    1. **Adaptor Driver** - this talks with the st-link v2 via USB. It can send code (aka the ST-link is a programmer), and can also talk with the MCU directly to do debugging(so the ST-link is also a debugger). It supports both the ST-link v2, and also J-link, an alternative debugger hardware. 
    1. **Code Editor** - this is the actual place I write my code. It's based on Eclipse, a popular IDE, and according to ST's website, can support Eclipse plugins
    1. **Middleware** - this is all the code written by ST to make programming STM32 microcontrollers easier. ST calls them STM32cube MCU/MPU packages. These include the Hardware Abstraction Layer (HAL), Low-Layer (LL) APIs, and various libraries to support things like Real-time operating systems (RTOS), USB, file systems, etc. It also has a GUI that helps you with your initial setup of the different pins of a microcontroller. E.g. setting a particular pin to be a GPIO output pin. The STM32Cube IDE has packages for each of the STM32 families it supports. It's a lot of code
    1. **Compiler/linker** - this is the ARM GCC toolchain. This is the bit that actually compiles your C code into something the STM32 ARM microcontroller can actually run
    1. **Debug software** - the STM32Cube IDE supports using GDB as the debugger, which is a common C debugger tool. It also has extra debug support, like supporting RTOS debugging. 


### The Hardware Side
There's apparently a lot of places to get the hardware side, and for relatively cheap. But a lot of the places seem to be "Aliexpress" and "Ebay", and it feels like the quality control and speed of delivery for those both can be lacking. So instead, since I buy so much from Adafruit anyway, I decided to get my software from there. 

ST-link V2 from adafruit: [https://www.adafruit.com/product/2548](https://www.adafruit.com/product/2548)
We Act Studio STM32F411 "BlackPill" Development Board [https://www.adafruit.com/product/4877](https://www.adafruit.com/product/4877)

### The Software Side

I'm using the STM32Cube IDE, which is nice because it's all in one package to download. Download the IDE from: [https://www.st.com/en/development-tools/stm32cubeide.html](https://www.st.com/en/development-tools/stm32cubeide.html)


### The Code


### Sending Code

Final code for a simple blinky using the STM32CubeIDE with the We Act STM32F411 "black pill":

{% highlight c %}
 while (1)
  {
    /* USER CODE END WHILE */
	  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, 0);
	  HAL_Delay(1000);
	  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, 1);
	  HAL_Delay(1000);

    /* USER CODE BEGIN 3 */
  }
{% endhighlight %}

Note that I'm setting pin 13 to 0 to turn it ON, and 1 to turn it OFF. If you don't believe me, try changing the delay after the first `WritePin` to `5000` and see if it stays on or off longer. This is a result of how the LED is wired on the black pill board. If you look at the schematics for the board, you can see that the LED circuit is actually connected to 3.3 volts, then a resistor, then the LED, then PC13. This means when PC13 is low (set to `0`), it acts as ground, and the 3.3 volts move through the circuit. 