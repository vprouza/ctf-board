# This program was created in Arduino Lab for MicroPython

#print('Hello, MicroPython!')
# check if the device woke from a deep sleep
#if machine.reset_cause() == machine.DEEPSLEEP_RESET:
#    print('woke from a deep sleep')


import esp
import time
import network
import ubinascii
from machine import Pin, I2C, PWM, deepsleep

time.sleep(1)

blue = Pin(5,Pin.OUT)
blue.value(1)


def blink(pin, num):
  for i in range(num):
    pin.value(0)
    time.sleep(0.1)
    pin.value(1)
    time.sleep(0.1)


blink(blue,3)

def pad_time(int_time):
  if(int_time > 9):
    return str(int_time)
  else:
    return "0" + str(int_time)


def setup_wifi():
  wlan_id = "MikroTik-wAP"
  wlan_pass = "hesloheslo"

  mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
  print("MAC: " + mac)

  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  while wlan.status() is network.STAT_CONNECTING:
      time.sleep(1)
  while not wlan.isconnected():
      wlan.connect(wlan_id, wlan_pass)
  print("Connected... IP: " + wlan.ifconfig()[0])  



from ds3231 import DS3231

i2c = I2C(sda=Pin(8), scl=Pin(10))
ds = DS3231(i2c)
f = open("bootlog.txt", "a")
curdate = ds.datetime()
timestampstr = pad_time(curdate[0]) + "-" + pad_time(curdate[1]) + "-" + pad_time(curdate[2])+ "T" + pad_time(curdate[4])+ ":" + pad_time(curdate[5])+ ":" + pad_time(curdate[6])
print("Time: "+ timestampstr)
f.write(timestampstr + "\n")
f.close()


#deepsleep(5000)


def main():
  time.sleep(1)