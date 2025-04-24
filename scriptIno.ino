#include <Wire.h>
#include <LiquidCrystal_I2C.h>


LiquidCrystal_I2C lcd(0x27, 16, 2);  

void setup() {
  
  lcd.begin(16, 2);
  lcd.init();
  lcd.backlight();
 
  Serial.begin(9600);

  
  lcd.setCursor(0, 0);
  lcd.print("Aguardando gesto...");
}

void loop() {
  if (Serial.available() > 0) {
   
    String gesto = Serial.readString();

   
    lcd.clear();
    lcd.setCursor(0, 0);  
    lcd.print(gesto);
  }
}
