#include <Wire.h>
#include <EVShield.h>
#include <EVs_NXTTouch.h>
EVShield evshield(0x34,0x36);

int data;

void setup()
{
  Serial.begin(115200);  // start serial for output
  delay(500); // wait, allowing time to activate the serial monitor

  evshield.init(); // the default is SH_HardwareI2C

  evshield.bank_a.motorReset();
  evshield.bank_b.motorReset();
}


void loop()
{
  if (Serial.available() > 0)
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

}

void runMotor (int power)
{
  evshield.bank_b.motorRunUnlimited(SH_Motor_1, SH_Direction_Reverse, power);
  evshield.bank_a.motorRunUnlimited(SH_Motor_1, SH_Direction_Reverse, power); 
}

void stopMotor()
{
  evshield.bank_b.motorStop(SH_Motor_1, SH_Next_Action_Float);
  evshield.bank_a.motorStop(SH_Motor_1, SH_Next_Action_Float);
}
