
https://cdn-shop.adafruit.com/datasheets/pec11.pdf 
https://cdn.sparkfun.com/datasheets/Robotics/How%20to%20use%20a%20quadrature%20encoder.pdf
https://diyrobocars.com/2020/05/04/arduino-serial-plotter-the-missing-manual/
https://learn.adafruit.com/pro-trinket-rotary-encoder/example-rotary-encoder-volume-control
https://web.archive.org/web/20120208215116/http://www.circuitsathome.com/mcu/reading-rotary-encoder-on-arduino 
https://cdn-learn.adafruit.com/assets/assets/000/046/211/original/Huzzah_ESP8266_Pinout_v1.2.pdf?1504807178

Rotary encoder test
```
#define PIN_ENCODER_A      4
#define PIN_ENCODER_B      5

void setup() {
  Serial.begin(115200);
  pinMode(PIN_ENCODER_A, INPUT_PULLUP);
  pinMode(PIN_ENCODER_B, INPUT_PULLUP);

}

void loop() {
  int valA = digitalRead(PIN_ENCODER_A);
  int valB = digitalRead(PIN_ENCODER_B);

  //since these are default HIGH (aka have a pullup resistor)
  //either being set to LOW means something is happening on the encoder
  if (valA == LOW || valB == LOW){
    Serial.print(valA);
    Serial.print(" ");
    Serial.println(valB);
  }

}
```


Turned clockwise

|pin A |pin B |
|-----|-----|
|1 | 1 |
|0 | 1 |
|0 | 0 |
|1 | 0 |
|1 | 1 |

So in order, if set first bit to pinB and second bit to pinA (aka pin A=1, pin B=0 means binary number 10), the decimal equivalent is:
3, 1, 0, 2, 3

So the encoder is going clockwise if:
```
3->1
1->0
0->2
2->3
```

turned counter clockwise

|pin A |pin B |
|-----|-----|
| 1 | 1 |
| 1 | 0 |
| 0 | 0 |
| 0 | 1 |
| 1 | 1 |


3, 2, 0, 1, 3

And it's going counter clockwise if:
```
3->2
2->0
0->1
1->3
```

so lets do 1 means clockwise and -1 means counter clockwise I can list out all possible combinations of a previous and current value, and determine which way I'm going, or if I'm missing anything
| prev | cur | direction |
|---|---|---|
| 0 | 0 | UNDEFINED |
| 0 | 1 | -1 |
| 0 | 2 | 1 |
| 0 | 3 | UNDEFINED |
| 1 | 0 | 1 |
| 1 | 1 | UNDEFINED |
| 1 | 2 | UNDEFINED |
| 1 | 3 | -1 |
| 2 | 0 | -1 |
| 2 | 1 | UNDEFINED |
| 2 | 2 | UNDEFINED |
| 2 | 3 | 1 |
| 3 | 0 | UNDEFINED |
| 3 | 1 | 1 |
| 3 | 2 | -1 |
| 3 | 3 | UNDEFINED |

Based on this, I can see there's a lot of options that don't mean the encoder went clockwise OR counter clockwise. There's two separate groups of undefined values. If the previous and current values from the encoder are the same, that just means I read the values so fast, it didn't have time to change (or in the case of 3, the encoder isn't moving at all). So those just mean it didn't move. For the other group of undefined values, they're harder to categorize. Going from 0 to 3 means EITHER I moved clockwise so fast I went from 0 to 2 to 3 before my code had a chance to read the encoder values, OR I moved it _counter_ clockwise so fast I went from 0 to **1** to 3. So that tells me the encoder rotated, but I don't know which way! 




| | 0 | 1 | 2 | 3 |
| 0 | DIDN'T MOVE | -1 | 1 | SKIPPED A VALUE |
| 1 | 1 | DIDN'T MOVE | SKIPPED A VALUE | -1 |
| 2 | -1 | SKIPPED A VALUE | DIDN'T MOVE | 1 |
| 3 | SKIPPED A VALUE | 1 | -1 | DIDN'T MOVE |


Made lookup table:
```
{0, -1, 1, 2}
{1, 0, 2, -1}
{-1, 2, 0, 1}
{2, 1, -1, 0}
```


Code to see if this works:

{% highlight c++ %}
#define PIN_ENCODER_A      4
#define PIN_ENCODER_B      5

int prevVal = 0;
int newVal;

int lookupTable[4][4] = { {0, -1, 1, 2},
{1, 0, 2, -1},
{-1, 2, 0, 1},
{2, 1, -1, 0} };

void setup() {
  Serial.begin(115200);
  pinMode(PIN_ENCODER_A, INPUT_PULLUP);
  pinMode(PIN_ENCODER_B, INPUT_PULLUP);

  int valA = digitalRead(PIN_ENCODER_A);
  int valB = digitalRead(PIN_ENCODER_B);
  prevVal = (valA << 1) + valB;

}

void loop() {
  int valA = digitalRead(PIN_ENCODER_A);
  int valB = digitalRead(PIN_ENCODER_B);
  newVal = (valA << 1) + valB;

  int info = lookupTable[prevVal][newVal];


  if (info == 1){
    Serial.print("clockwise ");
    Serial.print(prevVal);
    Serial.print("->");
    Serial.println(newVal);
  }
  else if (info == -1){
    Serial.print("counter clockwise ");
    Serial.print(prevVal);
    Serial.print("->");
    Serial.println(newVal);
  }
  else if (info == 2){
    Serial.println("skipped a value");
  }
  
  prevVal = newVal;
}
{% endhighlight %}

This correctly understands clockwise and counterclockwise movement. HOWEVER, there's two issues. One, it's triggering roughly 4 times each detent, and Two sometimes the code manages to get a bounce or something else wonky, and it reads, say, 3 clockwise and one counterclockwise movement. So I want to track all the states it passes through, and then figure out which way its going, ignoring those occasional misreads.

>**NOTE** "detent" is a fancy word for that "click" feeling you get with rotary encoders. Each "click" position is a detent.


{% highlight c++ %}

#define PIN_ENCODER_A      4
#define PIN_ENCODER_B      5

int prevVal = 0;
int newVal;
unsigned int clockState = 0;
unsigned int counterClockState = 0;

//lookup table, first index is previous value
//second index is current value
//says if it's part of the sequence when moving
//clockwise (1) or counterclockwise (-1)
//didn't move (0) or skipped a value (2)
int lookupTable[4][4] = { {0, -1, 1, 2},
{1, 0, 2, -1},
{-1, 2, 0, 1},
{2, 1, -1, 0} };

void setup() {
  Serial.begin(115200);
  pinMode(PIN_ENCODER_A, INPUT_PULLUP);
  pinMode(PIN_ENCODER_B, INPUT_PULLUP);

  int valA = digitalRead(PIN_ENCODER_A);
  int valB = digitalRead(PIN_ENCODER_B);
  prevVal = (valA << 1) + valB;

}

void loop() {
  int valA = digitalRead(PIN_ENCODER_A);
  int valB = digitalRead(PIN_ENCODER_B);
  newVal = (valA << 1) + valB;
  
  int info = lookupTable[prevVal][newVal];


  if (info == 1){
    clockState |= (1 << newVal); //set the bit to 1
  }
  else if (info == -1){
    counterClockState |= (1 << newVal);
  }
  else if (info == 2){
    Serial.println("skipped a value");
  }

  if (prevVal != newVal && newVal == 3){
    //changed to the non moving state, lets figure out what direction we went!

    //for each clockwise and counterclockwise, the encoder state goes through 4 distinct states
    //make sure it's gone through at least 3 of those (and assume if one is missing it's because I didn't read fast enough)
    if (clockState == 0b1011 || clockState == 0b1101 || clockState == 0b1110 || clockState == 0b1111){
      Serial.println("Result was clockwise");
    }
    if (counterClockState == 0b1011 || counterClockState == 0b1101 || counterClockState == 0b1110 || counterClockState == 0b1111){
      Serial.println("Result was COUNTER clockwise");
    }
    
    clockState = 0;
    counterClockState = 0;
    
  }
  
  prevVal = newVal;
}
{% endhighlight %}