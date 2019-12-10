#include <SPI.h>
#include <Pixy2.h>
#include <Wire.h>
#include <EVShield.h>
#include <MemoryFree.h>
#include <pgmStrToRAM.h>

EVShield evshield(0x34,0x36);

// This is the main Pixy object 
Pixy2 pixy;

void setup()
{
  Serial.begin(115200);  
  pixy.init();
  
  evshield.init(); // the default is SH_HardwareI2C
  evshield.bank_a.motorReset();
  evshield.bank_b.motorReset();
}

void loop(){
  // grab blocks!
  pixy.ccc.getBlocks();
  int ageNeeded = 25;
  // If there are detect blocks, print them!
  if (pixy.ccc.numBlocks)
  {
    Block detectedObject = pixy.ccc.blocks[0];
    //Data to the serial is sent 
    //when the block has been seen more than 
    //ageNeeded amount of frames. 
    if(detectedObject.m_age > ageNeeded) { 
      sendData(detectedObject.m_x, detectedObject.m_y, detectedObject.m_width, detectedObject.m_height);
      sleepUntilSignal();
    }
  }  
}

void sendData(int x, int y, int width, int height){
  Serial.print("x:");
  Serial.print(x);
  Serial.print(", y:");
  Serial.print(y);
  Serial.print(", w:");
  Serial.print(width);
  Serial.print(", h:");
  Serial.print(height);
  Serial.print(",\n");

}

void sleepUntilSignal(){
  int signal;
  while(true){
    signal = Serial.read();
    switch (signal){
        case '0':
            runMotor(20);
            break;
        case '1':
            runMotor(30);
            break;
        case '2':
            runMotor(40);
            break;
        case '3':
            runMotor(50);
            break;
        case '4':
            runMotor(60);
            break;
        case '5':
            runMotor(70);
            break;
        case '6':
            runMotor(80);
            break;
        case '7':
            runMotor(90);
            break;
        case '8':
            runMotor(100);
            break;
        case '9':
            return;
        }
    }
}

void runMotor (int power)
{
  evshield.bank_b.motorRunUnlimited(SH_Motor_1, SH_Direction_Reverse, power);
  evshield.bank_a.motorRunUnlimited(SH_Motor_1, SH_Direction_Reverse, power); 
}
