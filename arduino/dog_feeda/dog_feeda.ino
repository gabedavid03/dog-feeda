void setup() {
  Serial.begin(9600); // Start serial communication at 9600 baud rate
}

void loop() {
  if (Serial.available() > 0) {
    String feed_rotations_str = Serial.readStringUntil('\n'); // Read the incoming data as a string until newline
    Serial.println("Performing " + feed_rotations_str +  " rotations"); // Echo back the received data
    int feed_rotations = feed_rotations_str.toInt();
  }
}