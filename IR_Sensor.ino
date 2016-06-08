#include <Wire.h> 
#include <SPI.h>
#include <RH_RF95.h>

#define RFM95_CS 10
#define RFM95_RST A1
#define RFM95_INT 2
#define RF95_FREQ 915.0

#define LED A2
#define IR A3
#define BATTERY_SENSE A0

RH_RF95 rf95(RFM95_CS, RFM95_INT);

int lastread = HIGH;
long counter = 0; //Blink counter
long txcounter = 0;
long lastblink = 0; //Time since last blink
long lastupdate = 0; //Time since last update
long avgwatts = 0;

String ident = "A1"; //Define Address of Sensor
int txpower = 5;


void setup() {
  pinMode(LED, OUTPUT);
  pinMode(IR, INPUT);
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  analogReference(INTERNAL);
  
  Serial.begin(9600);

  while (!Serial) {
    digitalWrite(LED, HIGH);
    delay(1500);
    digitalWrite(LED, LOW);
    delay(500);
  }

  while (!rf95.init()) {
    Serial.print("RADIO ERROR");
    digitalWrite(LED, HIGH);
    delay(1500);
    digitalWrite(LED, LOW);
    delay(500);
  }

  while (!rf95.setFrequency(RF95_FREQ)) {
    Serial.print("FREQ ERROR");
    digitalWrite(LED, HIGH);
    delay(1500);
    digitalWrite(LED, LOW);
    delay(500);
  }
}

void loop() {
  int ir_read = analogRead(IR);
  
  float sensorValue = analogRead(BATTERY_SENSE);
  float batteryV  = sensorValue * 0.003363075;
  float batteryPcnt = sensorValue / 10;
  
  String buffer;
  char txbuffer[31];
  String total_watts = "TW";
  String watts = "WC";
  String avg_watts = "AW";
  String vbuffer = "V";
  

  if (ir_read <= 100) {
    counter++;
    txcounter++;
    Serial.println(ir_read);
    delay(100);

    if (millis() >= lastupdate + 60000) {
      
      lastupdate = millis();
      avgwatts = (counter / (millis()/600000));

      watts = watts + txcounter;
      total_watts = total_watts + counter;
      avg_watts = avg_watts + avgwatts;
      vbuffer = vbuffer + batteryPcnt;

      txcounter = 0;

      buffer = ident + "," + total_watts + "," + watts + "," + avg_watts + "," + vbuffer;

      buffer.toCharArray(txbuffer, 31);

      Serial.print(counter);
      Serial.print("\t");
      Serial.println(avgwatts);
      Serial.println(txbuffer);

      rf95.setModeIdle();
      delay(10);

      rf95.send((uint8_t *)txbuffer, 31);
      delay(10);
      rf95.waitPacketSent();
      delay(10);
      rf95.sleep();
    }
  }
}

