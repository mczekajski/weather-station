from machine import Pin, I2C
from pico_i2c_lcd import I2cLcd
import utime
import bme280
import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests
import json

led = Pin('LED', Pin.OUT)
led.on()

# Connect to network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Fill in your network name (ssid) and password here:
ssid = 'YOUR_NETWORK_NAME'
password = 'YOUR_PASSWORD'
wlan.connect(ssid, password)

weather_data = {}
counter = 0

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

i2c0 = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
i2c1 = I2C(1, sda=machine.Pin(18), scl=machine.Pin(19), freq=400000)

lcd = I2cLcd(i2c0, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
bme = bme280.BME280(i2c=i2c1)

def load_weather_data():
    r = urequests.get("http://api.openweathermap.org/data/2.5/weather?q=Sosnowiec&appid={YOUR_API_CODE}&lang=pl")
    global weather_data
    weather_data = json.loads(r.text)['main']

def type_machine(str):
    split = list(str)
    for letter in split:
        lcd.putstr(letter)
        utime.sleep(.1)

def kelvin_to_celsius(kelvin):
  return kelvin - 273.15
    
        
def print_internal_conditions():
    lcd.clear()
    lcd.putstr('INTERNAL CONDITIONS')
    lcd.move_to(0,1)
    lcd.putstr('Temperature ' + str(round(float(bme.values[0]),1)) + ' C')
    lcd.move_to(0,2)
    lcd.putstr('Pressure    ' + str(round(float(bme.values[1])+260/7.888)) + ' hPa')
    lcd.move_to(0,3)
    lcd.putstr('Humidity    ' + str(round(float(bme.values[2]))) + ' %')

def print_external_conditions():
    print(weather_data)
    lcd.clear()
    lcd.putstr('EXTERNAL CONDITIONS')
    lcd.move_to(0,1)
    lcd.putstr('Temperature ' + str(round(kelvin_to_celsius(weather_data['temp']),1)) + ' C')
    lcd.move_to(0,2)
    lcd.putstr('Pressure    ' + str(weather_data['pressure']) + ' hPa')
    lcd.move_to(0,3)
    lcd.putstr('Humidity    ' + str(weather_data['humidity']) + ' %')

# Weather station init
lcd.clear()
lcd.hide_cursor()
type_machine('WEATHER STATION v1.1')
utime.sleep(2)
        
# Infinite loop
while True:
    if (counter % 5 == 0):
        load_weather_data()
        counter = 0
    print_internal_conditions()
    utime.sleep(10)
    print_external_conditions()
    utime.sleep(10)
    counter += 1
