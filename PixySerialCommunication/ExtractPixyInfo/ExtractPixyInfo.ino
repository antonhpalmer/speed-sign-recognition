#include <Pixy2.h>

// This is the main Pixy object 
Pixy2 pixy;

void setup()
{
  Serial.begin(115200);  
  pixy.init();
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
      }
      //pixy.ccc.blocks[i].print();
    }
  }  
}
