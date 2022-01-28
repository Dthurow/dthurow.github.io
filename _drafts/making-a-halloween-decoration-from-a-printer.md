




https://learn.sparkfun.com/tutorials/experiment-guide-for-the-sparkfun-tinker-kit/experiment-9-driving-a-motor-with-an-h-bridge


Code to get motor driver working and reading from serial:

//define the two direction logic pins and the speed / PWM pin
const int DIR_A = 5;
const int DIR_B = 4;
const int PWM = 6;
int motorSpeed;
bool ForwardRotation = true;

void setup() {
  //set all pins as output
  pinMode(DIR_A, OUTPUT);
  pinMode(DIR_B, OUTPUT);
  pinMode(PWM, OUTPUT);
  Serial.begin(115200);

}

void loop() {
  //check if new direction or speed
  if (Serial.available()) {
    int result = Serial.parseInt(SKIP_ALL);
    Serial.read(); //read newline
    Serial.print("Received: "); Serial.println(result);
    if (result < 0) {
      //going backwards
      motorSpeed = -result;
      ForwardRotation = false;
    }
    else {
      //going forward
      motorSpeed = result;
      ForwardRotation = true;
    }
  }

  if (ForwardRotation) {
    digitalWrite(DIR_A, HIGH);
    digitalWrite(DIR_B, LOW);
    analogWrite(PWM, motorSpeed);
  }
  else {
    digitalWrite(DIR_A, LOW);
    digitalWrite(DIR_B, HIGH);
    analogWrite(PWM, motorSpeed);
  }



}