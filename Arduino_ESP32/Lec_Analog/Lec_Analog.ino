void setup() 
{
  Serial.begin(115200);
  delay(100);

}



void loop() 
{
  int vLeido = analogRead(36);
  float valorReal = vLeido * (3.3/4096);

  float vResis = (5.0/valorReal+1)*4700*2;

  float vSiem = (1/vResis)*1000000;
  Serial.println(vSiem);
  delay(1000);
}