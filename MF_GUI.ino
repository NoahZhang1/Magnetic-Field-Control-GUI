String receivedData = "";  // Store the received string

void setup() {
  Serial.begin(9600);  // Initialize the serial port at 9600 baud rate
}

void loop() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();  // Read a character from the serial port

    if (inChar == '\n') {  // Check for the end of the string
      Serial.print("Received: ");
      Serial.println(receivedData);
      receivedData = "";  // Clear the string for new data
    } else {
      receivedData += inChar;// Append the received character to the string
    }

    receivedData += '\n';
  }
}
