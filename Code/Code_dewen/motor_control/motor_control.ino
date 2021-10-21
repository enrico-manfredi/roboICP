#include <Adafruit_MotorShield.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield();

Adafruit_DCMotor *myDC = AFMS.getMotor(1);

Adafruit_StepperMotor *myStepper = AFMS.getStepper(200,2);
void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps

  if (!AFMS.begin()) {
    Serial.println("Could not find Motor Shield. Check wiring.");
    while (1);
  }
  Serial.println("Motor Shield found.");

  // Set the speed to start, from 0 (off) to 255 (max speed)
  myDC->setSpeed(255);
  myStepper -> setSpeed(1);
}

void loop() {
 if(Serial.available()>0) {
  char index = Serial.read();
  if ((index >= '0') && (index <= '5')){
    Serial.println("Rotating Feeder");
    myStepper -> step(100, BACKWARD, DOUBLE);
    delay(5000);
     
    Serial.println("stiring");
    myDC -> run(FORWARD);
    delay(10000);
    myDC -> run(RELEASE);
  }
 }
}
