/*
Title
: Home automation using blynk
Description : To control light's brigntness with brightness,monitor
temperature , monitor water level in the tank through blynk app
Pheripherals : Arduino UNO , Temperature system, LED, LDR module,
Serial Tank, Blynk cloud, Blynk App.
*/
// Template ID, Device Name and Auth Token are provided by the
Blynk.Cloud
// See the Device Info tab, or Template settings
#define BLYNK_TEMPLATE_ID "*******"
#define BLYNK_DEVICE_NAME "********"
#define BLYNK_AUTH_TOKEN "*************"
// Comment this out to disable prints
#define BLYNK_PRINT Serial
#include <SPI.h>
#include <Ethernet.h>
#include <BlynkSimpleEthernet.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "main.h"
#include "temperature_system.h"
#include "ldr.h"
#include "serial_tank.h"
char auth[] = BLYNK_AUTH_TOKEN;
bool heater_sw,inlet_sw,outlet_sw;
unsigned int tank_volume;
BlynkTimer timer;
LiquidCrystal_I2C lcd(0x27, 16, 2); // set the LCD address to 0x27 for a
16 chars and 2 line display// This function is called every time the Virtual Pin 0 state changes
/*To turn ON and OFF cooler based virtual PIN value*/
BLYNK_WRITE(COOLER_V_PIN)
{
}
/*To turn ON and OFF heater based virtual PIN value*/
BLYNK_WRITE(HEATER_V_PIN )
{
}
/*To turn ON and OFF inlet vale based virtual PIN value*/
BLYNK_WRITE(INLET_V_PIN)
{
}
/*To turn ON and OFF outlet value based virtual switch value*/
BLYNK_WRITE(OUTLET_V_PIN)
{
}
/* To display temperature and water volume as gauge on the Blynk App*/
void update_temperature_reading()
{
// You can send any value at any time.
// Please don't send more that 10 values per second.
}
/*To turn off the heater if the temperature raises above 35 deg C*/
void handle_temp(void)
{
}
/*To control water volume above 2000ltrs*/
void handle_tank(void)
{
}
void setup(void){
}
void loop(void)
{
}
/*
Blink
Turns an LED on for one second, then off for one second, repeatedly.
Most Arduinos have an on-board LED you can control. On the UNO,
MEGA and ZERO it is attached to digital pin 13, on NODEMCU on pin 6.
LED_BUILTIN is set to the correct LED pin independent of which board
is used.If you want to know what pin the on-board LED is connected to on
your Arduino
*/
#define LED_BUILTIN
2
// the setup function runs once when you press reset or power the board
// the setup function runs once when you press reset or power the board
void setup() {
// initialize digital pin LED_BUILTIN as an output.
pinMode(LED_BUILTIN, OUTPUT);
  }
// the loop function runs over and over again forever
void loop() {
digitalWrite(LED_BUILTIN, HIGH); // turn the LED on (HIGH is the
voltage level)
delay(1000);
// wait for a second
digitalWrite(LED_BUILTIN, LOW); // turn the LED off by making the
voltage LOW
delay(1000);
// wait for a second
}/*
Title
: CLCD
Description : To configure the CLCD
*/
/*To use i2c protocol and uilt in LCD libraray*/
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
/* set the LCD address to 0x27 for a 16 chars and 2 line display*/
LiquidCrystal_I2C lcd(0x27, 16, 2);
void setup(void)
{
/*initialize the lcd*/
lcd.init();
lcd.backlight();
lcd.clear();
lcd.home();
/*To display string*/
lcd.setCursor(0, 0);
lcd.print("Home automation");
delay(1000);
}
void loop(void)
{
}
/*To control the brightness of the led using PWM(analogwrite)*/
const int analog_ip = A1;
const int LED = 3;
int inputVal = 0;
void setup() {
pinMode (LED, OUTPUT);
}
void loop() {
inputVal = analogRead(analog_ip);
  analogWrite (LED, inputVal/4);
delay(1000);
}
/*To read the analog values and print it on the Serial monitor*/
void setup()
{
// put your setup code here, to run once:
Serial.begin(9600);
}
void loop()
{
// put your main code here, to run repeatedly:
unsigned int adc_val;
static unsigned int pre_val=0;
adc_val = analogRead(A0);
if (pre_val != adc_val)
{
pre_val = adc_val;
Serial.println(adc_val);
  }
delay(1000);
}
/*To use i2c protocol and uilt in LCD libraray*/
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
/* set the LCD address to 0x27 for a 16 chars and 2 line display*/
LiquidCrystal_I2C lcd(0x27, 16, 2);
//input digital
#define INLET_VALVE 0x00
#define OUTLET_VALVE 0x01
//sensors digital
#define HIGH_FLOAT 0x10
#define LOW_FLOAT 0x11
//sensor analog
#define VOLUME 0x30
#define ENABLE 0x01
#define DISABLE 0x00
unsigned int value, value1;
void setup(void) {
Serial.begin(19200);
/*initialize the lcd*/
lcd.init();
lcd.backlight();
lcd.clear();
lcd.home();
lcd.setCursor(0, 0);
lcd.print(" Connect srtank");
/*synchronise communication*/
Serial.write(0xFF);
Serial.write(0xFF);
Serial.write(0xFF);
}
unsigned char valueh, valuel;
char buff[6];
void volume(void) {
Serial.write(VOLUME);
while(!Serial.available());
valueh = Serial.read();
while(!Serial.available());
valuel = Serial.read();
value = (valueh << 8) | valuel;
lcd.setCursor(0, 1);
lcd.print("v=");
lcd.print(value);
lcd.print("l ");
}
void filling_start(void){
Serial.write(INLET_VALVE);
  Serial.write(ENABLE);
Serial.write(OUTLET_VALVE);
Serial.write(DISABLE);
lcd.setCursor(0, 0);
lcd.print("Filling ");
//delay(1000);
do {
Serial.write(HIGH_FLOAT);
while(!Serial.available());
value1 = Serial.read();
volume();
} while (value1 == 0);
}
void start_emptying(void)
{
Serial.write(OUTLET_VALVE);
Serial.write(ENABLE);
Serial.write(INLET_VALVE);
Serial.write(DISABLE);
lcd.setCursor(0, 0);
lcd.print("Emptying");
//delay(1000);
do {
Serial.write(LOW_FLOAT);
  while(!Serial.available());
value1 = Serial.read();
volume();
} while (value1 == 1);
}
void loop(void)
{
filling_start();
//delay(10000);
start_emptying();
}
