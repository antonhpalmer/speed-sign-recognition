#include <SPI.h>
#include <Pixy2.h>
#include <Wire.h>
#include <EVShield.h>

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


void loop()
{ 
  int ageNeeded = 25;
  // grab blocks!
  pixy.ccc.getBlocks();
  
  // If there are detect blocks, print them!
  if (pixy.ccc.numBlocks)
  {
    Block detectedObject = pixy.ccc.blocks[0];
    
    //Data to the serial is sent 
    //when the block has been seen more than 
    //ageNeeded amount of frames. 
    if(detectedObject.m_age > ageNeeded) { 
      Serial.print("x:");
      Serial.print(detectedObject.m_x);
      Serial.print(", y:");
      Serial.print(detectedObject.m_y);
      Serial.print(", w:");
      Serial.print(detectedObject.m_width);
      Serial.print(", h:");
      Serial.print(detectedObject.m_height);
      Serial.print(",\n");
      sleepUntilSignal();
    }
  }  
}

void sleepUntilSignal(){
  int signal;
  while(true){
    signal = Serial.read();
    if (signal == '0') //30 km sign
      runMotor(20);
    else if (signal == '1') //50 km sign
      runMotor(30);
    else if (signal == '2') //60 km sign
      runMotor(40);
    else if (signal == '3') //70 km sign
      runMotor(50);
    else if (signal == '4') //80 km sign
      runMotor(60);
    else if (signal == '5') //90 km sign
      runMotor(70);
    else if (signal == '6') //100 km sign
      runMotor(80);
    else if (signal == '7') //110 km sign
      runMotor(90);
    else if (signal == '8') //120 km sign
      runMotor(100);
    else if (signal == '9') //wakeup signal
      return;
  }
}

void runMotor (int power)
{
  evshield.bank_b.motorRunUnlimited(SH_Motor_1, SH_Direction_Reverse, power);
  evshield.bank_a.motorRunUnlimited(SH_Motor_1, SH_Direction_Reverse, power); 
}
