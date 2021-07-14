


This as base: https://learn.adafruit.com/buzzing-mindfulness-bracelet/overview


need to include libraries from: https://learn.adafruit.com/adafruit-gemma-m0/circuitpython-libraries


Use troubleshooting to determine dotstar info: https://learn.adafruit.com/adafruit-gemma-m0/troubleshooting 

Use this to connect with repl and see error: https://learn.adafruit.com/welcome-to-circuitpython/advanced-serial-console-on-mac-and-linux

screen /dev/ttyACM0 115200

Error was:
    main.py output:
    Traceback (most recent call last):
    File "main.py", line 9, in <module>
    ImportError: no module named 'adafruit_dotstar'

added dotstar library, now error:

    main.py output:
    Traceback (most recent call last):
    File "main.py", line 9, in <module>
    File "adafruit_dotstar.py", line 22, in <module>
    ImportError: no module named 'adafruit_pypixelbuf'

added pypixelbuf library, code now works


Initially had only one coin battery, didn't work. Need more juice, because USB works fine. Double checked docs, turns out it needs 4-6 Volts. one coin battery is 3.3. 

Cann connect two coin batteries in serial to increase voltage amount: https://www.power-sonic.com/blog/how-to-connect-batteries-in-series-and-parallel/ 

negative terminal on one goes to positive of the other. the free positive and free negative attach to the microcontroller

Once connected, it seems to work




Calculating voltage and current use needed for circuit
### 

Gemma M0 broken down into individual parts as understood from schematic here: [https://cdn-learn.adafruit.com/assets/assets/000/044/361/original/gemma_schem.png?1501106076](https://cdn-learn.adafruit.com/assets/assets/000/044/361/original/gemma_schem.png?1501106076)

| part No. | Part Type | voltage range | current use | Datasheet |
|------|---------------|-------------|-----------|
| ATSAMD21E18 | 32-bit ARM Cortex -M0+ processor |  1.62V – 3.63V | 3.11 - 3.64 mA | [https://cdn-learn.adafruit.com/assets/assets/000/044/363/original/samd21.pdf?1501106093](https://cdn-learn.adafruit.com/assets/assets/000/044/363/original/samd21.pdf?1501106093) |
| ap211k-3.3 | CMOS process low dropout linear regulator | 2.5V-6.0V |  55µA when quiescent aka .055mA | [https://www.diodes.com/assets/Datasheets/AP2112.pdf](https://www.diodes.com/assets/Datasheets/AP2112.pdf) |
| AP102-2020 | APA102 IC for the three-color RGB Dimming control strip and string | .3-6V | .1W-.5W aka 20mA-100mA according to [this watt to amp calculator](https://www.rapidtables.com/calc/electric/Watt_to_Amp_Calculator.html) | [https://cdn-shop.adafruit.com/product-files/3341/3341_APA102-2020+SMD+LED.pdf](https://cdn-shop.adafruit.com/product-files/3341/3341_APA102-2020+SMD+LED.pdf) |
| 100614 | Vibration motor |  2.5~3.8V (adafruit site says 2V - 5V) | 75 mA max (adafruit site has a larger range depending on voltage, from 40mA-100mA) | [https://cdn-shop.adafruit.com/product-files/1201/P1012_datasheet.pdf](https://cdn-shop.adafruit.com/product-files/1201/P1012_datasheet.pdf) |

So voltage needs to be between 2.5 and 6 volts.

For the vibration motor, it's not on all the time, so while it needs to be able to get 100mA max current when it's on, I shouldn't just add that in when calculating battery life. Instead, I need to figure out the duty cycle

>**NOTE** Duty cycle is the percentage a part is on and drawing power, for a given cycle

In my case, lets use the case where it buzzes the most, 1 buzz for 1 second, every 1 minute (ish). So that's 1 second per 60 seconds, which is 1/60, 1.66% of the time. If the vibration motor is pulling the max estimated current (100mA) for one second every minute, on average, it's drawing 1.67mA.

I have to also do this for the IC that controls the dotstar LEDs (part no. AP102-2020 in above table). This one has a max of 100mA current as well. In code, I'm turning on LEDs for a quarter of a second, to display info to end users. The max time the LED will flash is 10 times in a row (for 10 minute intervals).

Current use (taking the max current usage for some leeway) is:

(max current of SAMD21) + (max current of linear regulator) + (max current of dotstar RGB IC) + (average current of vibration motor)

3.64 mA + .055mA + 100mA + 1.67mA

105.365 mA


if the battery is 220mAh, then with this circuit, the batteries will last 220mAh/105.365mA = 2.08797988 hours