

Datasheet is here: [https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-2586-AVR-8-bit-Microcontroller-ATtiny25-ATtiny45-ATtiny85_Datasheet.pdf](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-2586-AVR-8-bit-Microcontroller-ATtiny25-ATtiny45-ATtiny85_Datasheet.pdf)


![pinout](/assets/using-attyiny85/Chip-Pinout.png)

Port B is a 6-bit bi-directional I/O port with internal pull-up resistors (selected for each bit)

Reset input. A low level on this pin for longer than the minimum pulse length will generate a reset


The Status Register contains information about the result of the most recently executed arithmetic instruction. This
information can be used for altering program flow in order to perform conditional operations. Note that the Status
Register is updated after all ALU operations, as specified in the Instruction Set Reference. This will in many cases
remove the need for using the dedicated compare instructions, resulting in faster and more compact code.
The Status Register is not automatically stored when entering an interrupt routine and restored when returning
from an interrupt. This must be handled by software.

When the AVR exits from an interrupt, it will always return to the main program and execute one more instruction
before any pending interrupt is served.

The interrupt execution response for all the enabled AVR interrupts is four clock cycles minimum

If an interrupt occurs when the MCU is in sleep mode, the interrupt execution response time is increased by four clock cycles. 

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

### Interrupts
The External Interrupts are triggered by the INT0 pin or any of the PCINT\[5:0] pins. Observe that, if enabled, the
interrupts will trigger even if the INT0 or PCINT\[5:0] pins are configured as outputs. 

The INT0 interrupts can be triggered by a falling or rising edge or a low level. This is set up as indicated in the
specification for the MCU Control Register – MCUCR.

### I/O Pins
Three I/O memory address locations are allocated for each port, one each for the Data Register – PORTx, Data
Direction Register – DDRx, and the Port Input Pins – PINx

 optional internal pull-ups.

 there's a summary at: 23. Register Summary which gives address