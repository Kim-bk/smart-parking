#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
SoftwareSerial RFID (D6, D5); // D6-TX (RFID), D5-RX (RFID)
// Replace with your network credentials
const char* ssid "Hoang Dat";
const char* pass "17062001";
const char* serverName = "http://192.168.0.106:7350/update-sensor";
unsigned long lastTime = 0;
unsigned long timerDelay = 5000;
#include <SPI.h>
#include <MFRC522.h>
#define SS_PIN D8
#define RST_PIN D0
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
MFRC522::MIFARE_Key key;
// Init array that will store new NUID
byte nuidPICC[4];
void setup() {
 Serial.begin(115200);
 SPI.begin(); // Init SPI bus
 rfid.PCD_Init(); // Init MFRC522
 Serial.println();
 Serial.print(F("Reader :"));
 rfid.PCD_DumpVersionToSerial();
 for (byte i = 0; i < 6; i++) {
   key.keyByte[i] = 0xFF;
 }
 Serial.println();
 Serial.println(F("This code scan the MIFARE Classic NUID."));
 Serial.print(F("Using the following key:"));
 printHex(key.keyByte, MFRC522::MF_KEY_SIZE);

 WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
 
  Serial.println("Timer set to 5 seconds (timerDelay variable), it will take 5 seconds before publishing the first reading.");
}
void loop() {
 // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
 if ( ! rfid.PICC_IsNewCardPresent())
   return;
 // Verify if the NUID has been readed
 if ( ! rfid.PICC_ReadCardSerial())
   return;
 Serial.print(F("PICC type: "));
 MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
 Serial.println(rfid.PICC_GetTypeName(piccType));
 // Check is the PICC of Classic MIFARE type
 if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&
     piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
     piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
   Serial.println(F("Your tag is not of type MIFARE Classic."));
   return;
 }
// if (rfid.uid.uidByte[0] != nuidPICC[0] ||
//     rfid.uid.uidByte[1] != nuidPICC[1] ||
//     rfid.uid.uidByte[2] != nuidPICC[2] ||
//     rfid.uid.uidByte[3] != nuidPICC[3] ) {
//   Serial.println(F("A new card has been detected."));
   // Store NUID into nuidPICC array
   for (byte i = 0; i < 4; i++) {
     nuidPICC[i] = rfid.uid.uidByte[i];
   }
   Serial.println(F("The NUID tag is:"));
   Serial.print(F("In hex: "));
   printHex(rfid.uid.uidByte, rfid.uid.size);
   Serial.println();
   Serial.print(F("In dec: "));
   printDec(rfid.uid.uidByte, rfid.uid.size);
   Serial.println();
 //}
 //else Serial.println(F("Card read previously."));
 // Halt PICC
 rfid.PICC_HaltA();
 // Stop encryption on PCD
 rfid.PCD_StopCrypto1();
}
/**
   Helper routine to dump a byte array as hex values to Serial.
*/
void printHex(byte *buffer, byte bufferSize) {
 for (byte i = 0; i < bufferSize; i++) {
   Serial.print(buffer[i] < 0x10 ? " 0" : " ");
   Serial.print(buffer[i], HEX);
 }
}
/**
   Helper routine to dump a byte array as dec values to Serial.
*/
void printDec(byte *buffer, byte bufferSize) {
 for (byte i = 0; i < bufferSize; i++) {
   Serial.print(buffer[i] < 0x10 ? " 0" : " ");
   Serial.print(buffer[i], DEC);
 }
}
