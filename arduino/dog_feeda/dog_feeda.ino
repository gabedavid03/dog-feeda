#include <HX711_ADC.h>

#define MOTOR_PIN 1
#define MOTOR_DIRECTION_PIN 2
#define HALL_PIN 3
#define HX711_dout 4
#define HX711_sck 5
#define SOLENOID_PIN 6

int motorSpe = 40;
int motorDir = 0;

HX711_ADC LoadCell(HX711_dout, HX711_sck); 
float water_full = 0; //need to set this to desired water level
unsigned long t = 0; 
static float water_mass; 

void HX711init(){
    bool _tare = true;
    unsigned long stabilizingtime = 2000; 
    LoadCell.start(stabilizingtime, _tare);
    if (LoadCell.getTareTimeoutFlag()) {
      Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
      while (1);
  }
    else {
      LoadCell.setCalFactor(calibrationValue); // set calibration value (float)
      Serial.println("Startup is complete");
  }
}

void water(){
  static bool newData = false; 
  cont int serialPrintInterval = 0; 

  if (LoadCell.update()){
    newData = true; 
    water_mass = LoadCekk.getData():
  }

  if(newData){
    if (millis() > t + serialPrintInterval){
      if(water_mass < water_full){
        digitalWrite(SOLENOID_PIN, LOW);
        while(water_mass < water_full){
          if (LoadCell.update()){
            water_mass = LoadCell.getData(); 
          }
        }
        digitalWrite(SOLENOID_PIN, HIGH);
      }
      Serial.print("Load_cell output val: ");
      Serial.println(water_mass);
      newData = False;
      t = millis();
  }
}
}

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
  HX711init(); 
}

void loop() {
  if (Serial.available() > 0) {
    String feed_rotations_str = Serial.readStringUntil('\n'); // Read the incoming data as a string until newline
    Serial.println("Performing " + feed_rotations_str +  " rotations"); // Echo back the received data
    int feed_rotations = feed_rotations_str.toInt();
    feed(feed_rotations);
  }
  water(); 
}