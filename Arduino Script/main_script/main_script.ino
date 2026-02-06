//notes//
//check command queing with python from the pi
//calibrate syringe positions
//print status messages to the LCD

#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <LiquidCrystal.h>
#include <Stepper.h>
#include <Servo.h>

//user variables//
//linear rail
int first_syringe = 18700;
int long next_syringe = 39600;
//lock servo
int lock_open = 95;
int lock_close = 5;
//tip servo
int tip_press = 0;
int tip_release = 40;
//liquid servo
int liq_press = 20;
int liq_press_hard = 0;
int liq_release = 100;
//hopper
int first_hole = 240;
int next_hole = 270;
//vibration motors
int vib_hop_s = 127; //caution - 255 will deliver 12V
int vib_plt_s = 127; //caution - 255 will deliver 12V
int stir_mot_s = 50; //caution - 255 will deliver 12V

//pins//
//outputs
int vial_dir = 49; //forward direction high
int vial_pls = 48; //rising edge pulse registration
int vial_ena = 47; //active low  - redundant
int rail_dir = 46; //forward direction high
int rail_pls = 45; //rising edge pulse registration
int rail_ena = 44; //active low - redundant
int actr_fw = 41; //IN3
int actr_bw = 40; //IN4
int pump_fw = 43; //IN1
int pump_bw = 42; //IN2
int shut_down = 53;
//Stepper
int hop_step_1 = 39; //in3
int hop_step_2 = 38; //in1
int hop_step_3 = 37; //in4
int hop_step_4 = 36; //in2
//LCD
const int rs = 34, en = 33, d4 = 32, d5 = 31, d6 = 30, d7 = 29;
//inputs
int rail_sw = 51;
int actr_sw_hi = 50;
int actr_sw_lo = 52;
//PWM
int vib_hop = 11;
int vib_plt = 12;
int stir_mot = 10;
int actr_en = 9; //ENB
int pump_en = 8; //ENA
int servo_1 = 7; //lock
int servo_2 = 6; //tip
int servo_3 = 5; //liquid
//onewire
int temp_sensors = 25;

//constants//
const int pos_rot = 640;
const int half_rot = pos_rot/2;
const int stepsPerRevolution = 2048;
const byte MAXIMUM_INPUT_LENGTH = 15;
const char PKG_START = '<';
const char PKG_END = '>';

//script variables//
int index = 0;
int pos = 0;
int first_feed = 1;
int shutdown_flag = 0;
int stp;
String input = "";
char currentInput = 0;
byte currentIndex = 0;

//objects//
Stepper hopStepper = Stepper(stepsPerRevolution, hop_step_1, hop_step_2, hop_step_3, hop_step_4);
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
#define ONE_WIRE_BUS temp_sensors
OneWire oneWire(ONE_WIRE_BUS);  
DallasTemperature sensors(&oneWire);
Servo servo1; //lock servo
Servo servo2; //tip servo
Servo servo3; //liquid servo

void setup() {
  //output setup//
  pinMode(rail_pls, OUTPUT);
  pinMode(rail_dir, OUTPUT);
  pinMode(rail_ena, OUTPUT);
  pinMode(vial_pls, OUTPUT);
  pinMode(vial_dir, OUTPUT);
  pinMode(vial_ena, OUTPUT);
  pinMode(actr_fw, OUTPUT);
  pinMode(actr_bw, OUTPUT);
  pinMode(pump_fw, OUTPUT);
  pinMode(pump_bw, OUTPUT);
  pinMode(shut_down, OUTPUT);
  pinMode(actr_en, OUTPUT);
  pinMode(pump_en, OUTPUT);

  //PWM output setup
  pinMode(vib_hop, OUTPUT);
  pinMode(vib_plt, OUTPUT);
  pinMode(stir_mot, OUTPUT);
  pinMode(actr_en, OUTPUT);
  pinMode(pump_en, OUTPUT);

  //input setup//
  pinMode(rail_sw, INPUT); //linear actuator home
  pinMode(actr_sw_hi, INPUT); //actuator upper
  pinMode(actr_sw_lo, INPUT); //actuator lower

  //peripherals setup//
  lcd.begin(16, 2);
  sensors.begin();
  hopStepper.setSpeed(5);
  servo1.attach(servo_1);
  servo2.attach(servo_2);
  servo3.attach(servo_3);

  //serial setup//
  Serial.begin(9600);
    while (!Serial) {
      ; // wait for serial port to connect. Needed for native USB port only
  }
    input = "";
  currentIndex = 0;
  
  if (Serial.available() > 0){
    currentInput = Serial.read();
    if (currentInput != PKG_START){
     //Serial.println(""); //debugs
     //Serial.println("<2>");
     //Serial.println("Started reading mid package, waiting for new start");
     while(currentInput != PKG_START){
      currentInput = Serial.read();
     }
    }
    while (currentInput != PKG_END and currentIndex < MAXIMUM_INPUT_LENGTH ){
      currentIndex += 1;
      input += currentInput;
      currentInput = Serial.read();
      //Serial.print("current input is:"); //debugs
      //Serial.println(currentInput);
      lcd.write(currentInput);
    }
  }
  //pin setup//
  digitalWrite(vial_pls, LOW);
  digitalWrite(vial_ena, HIGH);
  digitalWrite(rail_pls, LOW);
  digitalWrite(rail_ena, HIGH);
  //actuator h-bridge pins
  digitalWrite(actr_fw, LOW);
  digitalWrite(actr_bw, LOW);
  digitalWrite(actr_en, HIGH); //provides ability to pwm
  //pump h-bridge pins
  digitalWrite(pump_fw, LOW);
  digitalWrite(pump_bw, LOW);
  digitalWrite(pump_en, HIGH); //provides ability to pwm
  servo1.write(lock_open);
  servo2.write(tip_release);
  servo3.write(liq_release);
  //rxn system motor pins
  digitalWrite(vib_hop, LOW);
  digitalWrite(vib_plt, LOW);
  digitalWrite(stir_mot, LOW);

  //detach servos
  delay(1000);
  servo1.detach();
  servo2.detach();
  servo3.detach();
  
  //confirmation of setup end
  Serial.print(millis());
  Serial.print("\t");
  Serial.print("Setup complete");
  Serial.print("\n");
  lcd.setCursor(0,1);
  lcd.print("ready");
}

void loop() {
  delay(1); //stability delay
  //check system temperatures
  sensors.requestTemperatures();
  float temp0 = sensors.getTempCByIndex(0);
  float temp1 = sensors.getTempCByIndex(1);
  if (temp0 >= 60.0){
    shutdown_flag = 1;
  }
  else if (temp1 >= 60.0) {
    shutdown_flag = 1;
  }
  int index = 0;
  if (shutdown_flag == 1){
    index = 99;
  }
  else {
    if (Serial.available() > 0){
      index = Serial.parseInt();
    }
  }
  //special shutdown case
  if (index == 99){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    digitalWrite(shut_down, HIGH);
    delay(200);
    digitalWrite(shut_down, LOW);
  }
  //print all temperature values to serial monitor
  else if (index == 1){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print(" ");
    Serial.print(temp0);
    Serial.print(" ");
    Serial.print(temp1);
    Serial.print("\n");
  }
  //rot vial half position forward - 0.641s
  else if (index == 2){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    digitalWrite(vial_ena, LOW);
    delay(1);
    digitalWrite(vial_dir, HIGH);
    for (int i = 0; i <= half_rot; i++){
      digitalWrite(vial_pls, HIGH);
      delay(1);
      digitalWrite(vial_pls, LOW);
      delay(1);
    }
    digitalWrite(vial_ena, HIGH);
  }
  //rot vial half position backwards - 0.641s
  else if (index == 3){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    digitalWrite(vial_ena, LOW);
    delay(1);
    digitalWrite(vial_dir, LOW);
    for (int i = 0; i <= half_rot; i++){
      digitalWrite(vial_pls, HIGH);
      delay(1);
      digitalWrite(vial_pls, LOW);
      delay(1);
    }
    digitalWrite(vial_ena, HIGH);
  }
  //lin rail move to first syringe - 0.1ms/step
  else if (index == 4){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    digitalWrite(rail_ena, LOW);
    delay(1);
    digitalWrite(rail_dir, HIGH);
    for (int i = 0; i <= first_syringe; i++){
      digitalWrite(rail_pls, HIGH);
      delayMicroseconds(100);
      digitalWrite(rail_pls, LOW);
      delayMicroseconds(100);
    }
    digitalWrite(rail_ena, HIGH);
  }
  //lin rail move to next syringe - 0.1ms/step
  else if (index == 5){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    digitalWrite(rail_ena, LOW);
    delay(1);
    digitalWrite(rail_dir, HIGH);
    for (int i = 0; i <= next_syringe; i++){
      digitalWrite(rail_pls, HIGH);
      delayMicroseconds(100);
      digitalWrite(rail_pls, LOW);
      delayMicroseconds(100);
    }
    digitalWrite(rail_ena, HIGH);
  }
  //reset lin rail - 20s
  else if (index == 6){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    digitalWrite(rail_ena, LOW);
    delay(1);
    digitalWrite(rail_dir, LOW);
      for (int i = 0; i <= 200000; i++){
        if (digitalRead(rail_sw) == 1){
          break;
        }
        digitalWrite(rail_pls, HIGH);
        delayMicroseconds(100);
        digitalWrite(rail_pls, LOW);
        delayMicroseconds(100);
      }
      digitalWrite(rail_ena, HIGH);
    }
  //actuator backwards 0.1s
  else if (index == 7){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    if (digitalRead(actr_sw_hi) == 0){
     digitalWrite(actr_bw, HIGH);
     delay(100);
     digitalWrite(actr_bw, LOW); 
    }
  }
  //actuator forwards 0.1s
  else if (index == 8){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    if (digitalRead(actr_sw_lo) == 0){
     digitalWrite(actr_fw, HIGH);
     delay(100);
     digitalWrite(actr_fw, LOW); 
    }
  }
  //pump forwards for 0.1s
  else if (index == 9){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    digitalWrite(pump_fw, HIGH);
    delay(100);
    digitalWrite(pump_fw, LOW);  
  }
  //pump backwards for 0.1s
  else if (index == 10){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    digitalWrite(pump_bw, HIGH);
    delay(100);
    digitalWrite(pump_bw, LOW);  
  }
  //close lock servo - 0.5s
  else if (index == 11){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    servo1.attach(servo_1);
    servo1.write(lock_close);
    delay(1000);
    servo1.detach();
  }
  //open lock servo - 0.5s
  else if (index == 12){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    servo1.attach(servo_1);
    servo1.write(lock_open);
    delay(1000);
    servo1.detach();
  }
  //press tip release button 1s (2s total for release)
  else if (index == 14){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    servo2.attach(servo_2);
    servo2.write(tip_press);
    delay(1000);
    servo2.write(tip_release);
    delay(1000);
    servo2.detach();
  }
  //press liquid dispense button - 2.5s
  else if (index == 15){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    servo3.attach(servo_3);
    servo3.write(liq_press);
    delay(1500);
  }
  //move hopper to first hole from resting position - 0.5s
  else if (index == 16){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    hopStepper.step(-first_hole);
    delay(500);
  }

  //close the hopper +ve
  else if (index == 17){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    hopStepper.step(-next_hole/2);
    delay(500);
  }
  //shake hopper for 0.5s
  else if (index == 18){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    analogWrite(vib_hop, vib_hop_s);
    delay(500);
    digitalWrite(vib_hop, LOW);
  }
  //shake plate for 0.5s
  else if (index == 19){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    analogWrite(vib_plt, vib_plt_s);
    delay(500);
    digitalWrite(vib_plt, LOW);
  }
  //stir for 1s
  else if (index == 20){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    analogWrite(stir_mot, stir_mot_s);
    delay(1000);
    digitalWrite(stir_mot, LOW  );
  }
  //pulse linear actuator forwards for 0.1s
  else if (index == 21){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    while (digitalRead(actr_sw_lo) == 0){
     digitalWrite(actr_fw, HIGH);
     delay(100);
     digitalWrite(actr_fw, LOW); 
    }
  }
  //pulse linear actuator backwards for 0.1s
  else if (index == 22){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    while (digitalRead(actr_sw_hi) == 0){
     digitalWrite(actr_bw, HIGH);
     delay(100);
     digitalWrite(actr_bw, LOW);
    }
  }
  //stir for 25s
  else if (index == 23){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    analogWrite(stir_mot, stir_mot_s);
    delay(25000);
    digitalWrite(stir_mot, LOW);
  }
  //advance hopper halfway to next hole
  else if (index == 24){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    hopStepper.step(next_hole/2);
    delay(500);
  }
  //activate carousel stepper to hold position
  else if (index == 25){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    digitalWrite(vial_ena, LOW);
  }
  //release carousel stepper to prevent overheating
  else if (index == 26){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    digitalWrite(vial_ena, HIGH);
  }
  //press hard on the micropipette to release residual liquid
  else if (index == 27){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    servo3.attach(servo_3);
    servo3.write(liq_press_hard);
    delay(1500);
  }
  //remove pressure from the pipetting button
  else if (index == 28){
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(index);
    Serial.print("\n");
    servo3.write(liq_release);
    delay(1000);
    servo3.detach();
  }
}
