/*
(C) joukoy@gmail.com
Bluetooth <=> ALDL + Wideband O2 analog signal interface For Arduino MEGA 2560
Connect PC, phone or tablet to your Bluetooth module and use Bluetooth serial port in your application (Tunerpro, ALDLDroid etc)

#Required parts:
- Arduino Mega 2560 (or other Arduino model, need 2 free serial ports, or use softwareserial)
- Bluetooth module, for example HC-05, HC-06 or JDY-33
- 2 resistors, 100 ohm 

#Connections:

* Mega --- Bluetooth module *
Gnd --- Gnd
5v  --- Vcc
TX2 --- RX
RX2 --- TX

* Mega --- ALDL *
Tx3 -resistor 100R-\
                    ---- ALDL pin M
RX3 -resistor 100R-/
GND --- ALDL Pin A
Vin --- +12v when ign on (radio? Cigarette lighter?), or supply power to Arduino USB port

* Mega --- WB O2 sensor *
Gnd --- Gnd
A0  --- Analog out (0-5v)

#App settings
In tunerpro, add value for WB O2, use packet offset: 60, Source data size: 16 Bit 
If bytes 60 & 61 are used for something important, modify AFRByte below and packet offset to something else than 60 

Conversion for AEM X-series: (Need confirmation)
X*11.875/1023+7.3125  

Conversion for Innovate MTX-L (Totally untested)
X*15.04/1023 + 7.35

*/
#include <Arduino.h>
#define BtSerial Serial2
#define AldlSerial Serial3

const byte WBPin = A0;
const int AFRByte = 60;

//Note: Setup bluetooth module baudrate to 115200 OR modify BtBaudrate to match BT module baudrate
//Modify Tunerpro Acquistion settings to match baudrate
const unsigned long BtBaudrate = 115200; 
bool verbose = false;
bool echoCancel = true;

void setup() {
  AldlSerial.begin (8192);
  BtSerial.begin (BtBaudrate); 
  Serial.begin(115200);
  delay(100);
  Serial.write("Setup done\n");
}

void loop() {
  while (!BtSerial.available()) 
  {
    if (Serial.available())
    {
      char cmd = Serial.read();
      switch(cmd)
      {
      case 'v':
        verbose = true;
        Serial.println("Verbose mode on");
        break;
      case 'w':
        verbose = false;
        Serial.println("Verbose mode off");
        break;
      case 'e':
        echoCancel = true;
        Serial.println("Echo cancelling on");
        break;
      case 'f':
        echoCancel = false;
        Serial.println("Echo cancelling off");
        break;
      }
    }
    delay(2);
  }
  int cmdLen = 0;
  while (BtSerial.available()) 
  {
    while (BtSerial.available()) 
    {
      int cmdByte = BtSerial.read();
      AldlSerial.write(cmdByte);
      cmdLen++;
      if (verbose)
      {
        Serial.print(cmdByte, HEX);
        Serial.print(" ");
      }
    }  
    delay(2);
  }
  if (verbose)
  {
    Serial.println(" ");
  }
  AldlSerial.flush();
  int ALDLbyte = 0;                                                         // One byte of aldl data
  int DataStreamIndex = 0;                            
  long int start = millis();                      
  while (!AldlSerial.available()) 
  {
    delay(1);
    if ((millis() - start) > 400)
    {
      Serial.println("Timeout");
      break;
    }
  }

  int AFR = analogRead(WBPin);                          //Read WB voltage from analog pin (0-5v)
  if (verbose)
  {
    Serial.print("AFR: ");
    Serial.println(AFR);
  }
  while (AldlSerial.available() )                                          
  { 
      while (AldlSerial.available() )                    // Check for available data on the ALDL serial port
      {
        int dataByte = AldlSerial.read(); 
        if (DataStreamIndex == (AFRByte + cmdLen + 3))   // AFRByte + Sent bytes count (ALDL echo) + 3 header bytes
        {
          dataByte = (byte)(AFR >> 8);                  //Replace byte with MSB byte of AFR value
        }
        else if (DataStreamIndex == (AFRByte + cmdLen + 4))
        {
          dataByte = (byte)AFR;                       //Replace byte with LSB byte of AFR value
        }
        if (verbose)
        {
          Serial.print(dataByte, HEX);
          Serial.print(" ");
        }
        if (echoCancel == false || DataStreamIndex >= cmdLen) //Skip echo bytes if echoCancel = true
        {
          BtSerial.write(dataByte); 
        }
        DataStreamIndex++;                                          
      }     
      delay(3);
  }                                                                   
  if (verbose)
  {
    Serial.println(" ");
  }

}

