#include <math.h>
#include <LiquidCrystal.h>
#include <dht.h>

DHT sensor = DHT();

#define BUZZER_PIN 13
#define RED 12
#define GREEN 11
#define BLUE 10

LiquidCrystal lcd(2, 3, 4, 5, 6, 7);

void setup()
{
  Serial.begin(9600);

  lcd.begin(16, 2);

  sensor.attach(A1);

  delay(1000);
}

void loop()
{
  // thermistor
  int frequency;
  float voltage = analogRead(A0) * 5.0 / 1023.0;
  float r1 = voltage * 10000.0 / (5.0 - voltage);
  unsigned int B = 4300; // Параметр конкретного типа термистора (из datasheet)
  float temperature_tres = 1. / ( 1. / (B) * log(r1 / 10000.0) + 1. / 298. ) - 273; // 10KOm - R_25 // Температура с термистора

 
  frequency = map(temperature_tres, 26, 40, 3500, 4000);

  if (temperature_tres < 20.) {
    tone(BUZZER_PIN, frequency, 100);
    digitalWrite(GREEN, LOW);
    digitalWrite(BLUE, HIGH);
    digitalWrite(RED, LOW);
  }
  else if (temperature_tres > 25.) {
    tone(BUZZER_PIN, frequency, 100);
    digitalWrite(GREEN, LOW);
    digitalWrite(BLUE, LOW);
    digitalWrite(RED, HIGH);
  }
  else {
    digitalWrite(BUZZER_PIN, LOW);
    digitalWrite(GREEN, HIGH);
    digitalWrite(BLUE, LOW);
    digitalWrite(RED, LOW);
  }
Serial.print(temperature_tres,1);

// sensor

sensor.update();

char temperature_sensor[128];
char humidity_sensor[128];

sprintf(temperature_sensor, "%d.%d", sensor.getTemperatureInt(), sensor.getTemperatureFrac());
sprintf(humidity_sensor, "%d.%d", sensor.getHumidityInt(), sensor.getHumidityFrac());
Serial.print(" "); Serial.print(temperature_sensor); 
Serial.print(" "); Serial.println(humidity_sensor);

lcd.setCursor(0, 0);
lcd.print("T_tres: ");
lcd.print(temperature_tres, 1);
lcd.print(" ");
lcd.print((char)223);
lcd.print("C");

lcd.setCursor(0, 1);
lcd.print("T_sen: ");
lcd.print(temperature_sensor);
lcd.print(" ");
lcd.print((char)223);
lcd.print("C");
delay(2000);
lcd.clear();

// устанавливаем 1 станицу знакогенератора
lcd.command(0b101010);
lcd.print("H_sen: ");
lcd.print(humidity_sensor);
lcd.print("%");
delay(2000);
lcd.clear();
}
