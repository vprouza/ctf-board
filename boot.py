# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

from machine import Pin, I2C, PWM, ADC, deepsleep
from ds3231 import DS3231
import time
import os
import esp32


# output HIGH on Pin 4 to turn power on for peripherals

p4 = Pin(4,Pin.OUT,hold=True)
p4.value(1)
esp32.gpio_deep_sleep_hold(True)

# init pins for switch input
p6 = Pin(6,Pin.IN,Pin.PULL_UP)
p7 = Pin(7,Pin.IN,Pin.PULL_UP)

# init pins for RGB LED
blue = PWM(Pin(1,drive=Pin.DRIVE_1), freq=5000, duty=0)
green = PWM(Pin(2,drive=Pin.DRIVE_1), freq=5000, duty=0)
red = PWM(Pin(3,drive=Pin.DRIVE_1), freq=5000, duty=0)

# init ADC for battery readout
batt_adc = ADC(0)

# define i2c interface
i2c = I2C(sda=Pin(8), scl=Pin(10))
ds = DS3231(i2c)

def ledWrite(r,g,b):
  red.duty(int(r*4))
  green.duty(int(g*4))
  blue.duty(int(b*4))

def get_batt_v():
  return int(batt_adc.read_uv()*0.001762)

def get_sw_state():
  p6v = not p6.value()
  p7v = not p7.value()
  if p6v or p7v:
    if p6v:
      return 1
    if p7v:
      return 2
  else:
    return 0

def pad_time(int_time):
  if(int_time > 9):
    return str(int_time)
  else:
    return "0" + str(int_time)

def get_timestamp():
  curdate = ds.datetime()
  timestampstr = pad_time(curdate[0]) + "-" + pad_time(curdate[1]) + "-" + pad_time(curdate[2])+ "T" + pad_time(curdate[4])+ ":" + pad_time(curdate[5])+ ":" + pad_time(curdate[6])
  return timestampstr

def log_to_file(line):
  f = open("log.txt", "a")
  f.write(line + "\n")
  f.close()

def create_header():
  print("Creating new log.txt")
  f = open("log.txt", "a")
  f.write("timestamp;batt_mv;team" + "\n")
  f.close()

def delete_log():
  print("Deleting log.txt")
  os.remove("log.txt")
  create_header()

def go_to_sleep():
  print("Going to sleep in 1s")
  time.sleep(1)
  deepsleep()

def double_blink(r,g,b):
  ledWrite(r,g,b)
  time.sleep(0.2)
  ledWrite(0,0,0)
  time.sleep(0.2)
  ledWrite(r,g,b)
  time.sleep(0.1)
  ledWrite(0,0,0)

def long_blink(r,g,b):
  ledWrite(r,g,b)
  time.sleep(0.4)
  ledWrite(0,0,0)

def test_board():
  print("Running test")
  print("Sw middle")
  while get_sw_state() != 0:
    time.sleep(0.1)
  print("Sw up")
  while get_sw_state() != 1:
    time.sleep(0.1)
  print("Sw down")
  while get_sw_state() != 2:
    time.sleep(0.1)
  print("Sw middle")
  while get_sw_state() != 0:
    time.sleep(0.1)
  print("Datetime: " + str(get_timestamp()))
  print("Battvolt: " + str(get_batt_v()))
  ledWrite(255,0,0)
  time.sleep(2)
  ledWrite(0,255,0)
  time.sleep(2)
  ledWrite(0,0,255)
  time.sleep(2)
  ledWrite(0,0,0)
  print("Test finished")

# define colors in rgb
color_white = 50,50,50
color_green = 0, 128, 0
color_purple = 64, 0, 128

#color_red = 255,0,0
#color_red = 0,255,0
#color_red = 0,0,255

#colors for team neutral, 1 and 2
colors = [color_white,color_green,color_purple]
#colors = [color_red,color_green,color_blue]


def main():
  #print("Datetime: " + str(get_timestamp()))
  #print("Battvolt: " + str(get_batt_v()))

  #startup "animation"
  ledWrite(255,0,0)
  time.sleep(0.2)
  ledWrite(0,255,0)
  time.sleep(0.2)
  ledWrite(0,0,255)
  time.sleep(0.2)
  ledWrite(0,0,0)

  current_team = get_sw_state()
  capturing_team = current_team
  timer_start = None
  capture_delay = 5000

  if ds.datetime()[0] == 2000:
    ledWrite(255,255,0)
    return
  
  log_to_file(str(get_timestamp()) + ";" + str(get_batt_v()) + ";" + "-1")
  print(str(get_timestamp()) + ";" + str(get_batt_v()) + ";" + "-1")
  log_to_file(str(get_timestamp()) + ";" + str(get_batt_v()) + ";" + str(current_team))

  counter = 0

  while True:
    sw_state = get_sw_state()
    now = time.ticks_ms()

    if sw_state != capturing_team:
      capturing_team = sw_state
      timer_start = now

    if capturing_team != current_team:
      if timer_start is not None:
        elapsed_time = time.ticks_diff(now, timer_start)
        
        progress = elapsed_time / capture_delay
        if progress > 1.0:
          progress = 1.0

        r, g, b = colors[capturing_team]
        ledWrite(int(r * (progress ** 2)), int(g * (progress ** 2)), int(b * (progress ** 2)))

        if elapsed_time >= capture_delay:
          current_team = capturing_team
          log_to_file(str(get_timestamp()) + ";" + str(get_batt_v()) + ";" + str(sw_state))
          print(str(get_timestamp()) + ";" + str(get_batt_v()) + ";" + str(sw_state))
          
          long_blink(*colors[sw_state])
          timer_start = None
    
    else:
      timer_start = None
      
      counter += 1
      if counter > 10:
        double_blink(*colors[sw_state])
        counter = 0
      
    time.sleep(0.1)
  

main()