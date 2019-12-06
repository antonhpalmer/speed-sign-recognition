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

extern void *__bss_end;
extern void *__brkval;

int get_free_memory()
{
  int free_memory;

  if((int)__brkval == 0)
    free_memory = ((int)&free_memory) - ((int)&__bss_end);
  else
    free_memory = ((int)&free_memory) - ((int)__brkval);

  return free_memory;
}


void loop()
{ 
  /* Serial.print("Free memory:");
  Serial.print(get_free_memory());
  Serial.print("\n"); */
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
