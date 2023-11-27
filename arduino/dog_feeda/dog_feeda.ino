#include "HX711.h"

#define MOTOR_PIN 1
#define MOTOR_DIRECTION_PIN 2
#define HALL_PIN 3
#define LOADCELL_DOUT 4
#define LOADCELL_SCK 5
#define SOLENOID_PIN 6

int motorSpe = 40;
int motorDir = 0;

HX711 scale;
long calibration = 0; //need to find this value
float water_full = 0; //need to set this to desired water level


void feed(int rotations){
  int rotationCount = 0;
  int lastState = HIGH;

  while(rotationCount < rotations) {
    int currentState = digitalRead(HALL_PIN);
    // Detect the transition from LOW to HIGH (or HIGH to LOW)
    if(currentState != lastState) {
      if(currentState == HIGH) {
        rotationCount++;
      }
    lastState = currentState;
    }
    //move motor
    digitalWrite(MOTOR_PIN, HIGH);
    delay(motorSpe);
    digitalWrite(MOTOR_PIN, LOW);
    delay(motorSpe);
  }
  return;
}

void setup() {
  Serial.begin(9600); // Start serial communication at 9600 baud rate
  pinMode(MOTOR_PIN, OUTPUT);  //Assign Pind
  pinMode(MOTOR_DIRECTION_PIN, OUTPUT);
  pinMode(HALL_PIN, INPUT);
  pinMode(SOLENOID_PIN, OUTPUT);
  digitalWrite(SOLENOID_PIN, HIGH); //assuming normally open
  scale.begin(LOADCELL_DOUT, LOADCELL_SCK);
  scale.set_scale(calibration);
  scale.tare(); //setting scale to 0
}

void loop() {
  if (Serial.available() > 0) {
    String feed_rotations_str = Serial.readStringUntil('\n'); // Read the incoming data as a string until newline
    Serial.println("Performing " + feed_rotations_str +  " rotations"); // Echo back the received data
    int feed_rotations = feed_rotations_str.toInt();
    feed(feed_rotations);
  }

  float water_mass = scale.get_units();
  if(water_mass<water_full){
    digitalWrite(SOLENOID_PIN, LOW);
    while(water_mass<water_full){
      water_mass = scale.get_units();
    }
    digitalWrite(SOLENOID_PIN, HIGH);
  }
}