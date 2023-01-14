from machine import Pin, I2C
from pico_i2c_lcd import I2cLcd
import utime
import bme280

led = Pin('LED', Pin.OUT)
led.on()

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

i2c0 = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
i2c1 = I2C(1, sda=machine.Pin(18), scl=machine.Pin(19), freq=400000)

lcd = I2cLcd(i2c0, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
bme = bme280.BME280(i2c=i2c1)

def typeMachine(str):
    split = list(str)
    for letter in split:
        lcd.putstr(letter)
        utime.sleep(.1)

# Weather station init
lcd.clear()
lcd.hide_cursor()
typeMachine('Weather station 1.0')
utime.sleep(2)
        
# Infinite loop
while True:
    lcd.clear()
    lcd.putstr('INTERNAL CONDITIONS')
    lcd.move_to(0,1)
    lcd.putstr('Temperature ' + bme.values[0])
    lcd.move_to(0,2)
    lcd.putstr('Pressure  ' + bme.values[1])
    lcd.move_to(0,3)
    lcd.putstr('Humidity  ' + bme.values[2])
    utime.sleep(10)