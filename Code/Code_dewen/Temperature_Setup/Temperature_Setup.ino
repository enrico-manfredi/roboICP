
#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is plugged into digital pin 2 on the Arduino
#define ONE_WIRE_BUS 2

// Setup a oneWire instance to communicate with any OneWire device
OneWire oneWire(ONE_WIRE_BUS);  

// Pass oneWire reference to DallasTemperature library
DallasTemperature sensors(&oneWire);


int tempC;
int deviceCount = 0;
char index = 0;

void setup(void)
{
  sensors.begin();  // Start up the library
  Serial.begin(9600);
  deviceCount = sensors.getDeviceCount();
}


void loop(void) 
{ 
  // Send the command to get temperatures
  sensors.requestTemperatures(); 
  
  if (Serial.available()>0) {
    char convertor = '0';
    char index = Serial.read();
    int i = index - convertor;
    if ((index >= '0') && (index <= '5')) { 
      tempC = sensors.getTempCByIndex(i);
      Serial.println(tempC);
    }
  
    
  }
  //print the temperature in Celsius
  //Serial.print("Temperature: ");
  //Serial.println(sensors.getTempCByIndex(index));
  //Serial.print((char)176);//shows degrees character
  //Serial.print("C  |  ");
}
