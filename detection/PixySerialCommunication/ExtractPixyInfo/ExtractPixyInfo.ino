#include <SPI.h>

#include <Pixy2.h>
#include <Wire.h>
#include <EVShield.h>

EVShield evshield(0x34,0x36);

int data;

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
  int i; 
  int ageNeeded = 50;
  // grab blocks!
  pixy.ccc.getBlocks();
  
 
  // If there are detect blocks, print them!
  if (pixy.ccc.numBlocks)
  {
    for (i=0; i<pixy.ccc.numBlocks; i++)
    {
      if(pixy.ccc.blocks[i].m_age > ageNeeded) { //We first send the data to the serial when the block has been seen more than 100 frames. 
        //Serial.print(i);  
        Serial.print("x:");
        Serial.print(pixy.ccc.blocks[i].m_x);
        Serial.print(", y:");
        Serial.print(pixy.ccc.blocks[i].m_y);
        Serial.print(", w:");
        Serial.print(pixy.ccc.blocks[i].m_width);
        Serial.print(", h:");
        Serial.print(pixy.ccc.blocks[i].m_height);
        Serial.print(",\n");
        waitForSignal();
      }
      //pixy.ccc.blocks[i].print();
    }
  }
}


void waitForSignal(){
  while(true){
    data = Serial.read();
    
    if (data == '0')
      runMotor(20);
    else if (data == '1')
      runMotor(30);
    else if (data == '2')
      runMotor(50);
    else if (data == '3')
      runMotor(60);
    else if (data == '4')
      runMotor(70);
    else if (data == '5')
      runMotor(80);
    else if (data == '6')
      runMotor(90);
    else if (data == '7')
      runMotor(100);
    else if(data == '9'){
      break;
    }
  }
}

void runMotor (int power)
{
  evshield.bank_b.motorRunUnlimited(SH_Motor_1, SH_Direction_Reverse, power);
  evshield.bank_a.motorRunUnlimited(SH_Motor_1, SH_Direction_Reverse, power); 
}
