"""
 # MIT License
 # 
 # Copyright (c) 2024 Rahul Singh
 # 
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documentation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to whom the Software is
 # furnished to do so, subject to the following conditions:
 # 
 # The above copyright notice and this permission notice shall be included in all
 # copies or substantial portions of the Software.
 # 
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 # SOFTWARE.
 """

#!/usr/bin/python
 
import spidev
import time
import os
import serial


import RPi.GPIO as GPIO
from urllib2 import  urlopen


from email.MIMEMultipart import MIMEMultipart

from email import encoders

#BCM GPIO reference
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25,GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(21, GPIO.IN)
GPIO.setup(7, GPIO.IN)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
buzzer=12
#GPIO.setup(relay,GPIO.OUT)
GPIO.setup(buzzer,GPIO.OUT)
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  spi.max_speed_hz=1350000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Function to convert data to voltage level,
# rounded to specified number of decimal places.
"""def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts
 
# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
def ConvertTemp(data,places):
 
  # ADC Value
  # (approx)  Temp  Volts
  #    0      -50    0.00
  #   78      -25    0.25
  #  155        0    0.50
  #  233       25    0.75
  #  310       50    1.00
  #  465      100    1.50
  #  775      200    2.50
  # 1023      280    3.30
 
  temp = ((data * 330)/float(1023))-50
  temp = round(temp,places)
  return temp"""

 


gas_channel  = 0
status=0
 

delay = 1
flag =1
flag1=0
while True:
  flag =1
  u = urlopen("http://iotclouddata.com/project/723/getstatus.php")
  #f= io.TextIOWrapper(u,encoding='utf-8')
  text=u.read()
  print text
  #print text[9]
  if text[3]=='1':
        GPIO.output(19,1)
        print "Fan on"
        time.sleep(1)
  else :
        GPIO.output(19,0)
        print"Fan off"
        time.sleep(1)
  if text[4]=='1':
        GPIO.output(26,1)
        print "Light on"
        time.sleep(1)
  else :
        GPIO.output(26,0)
        print"Light off"
        time.sleep(1)
  if text[5]=='1':
        GPIO.output(13,1)
        print "Motor1 ON"
        time.sleep(1)
  else :
        GPIO.output(13,0)
        print"Motor1 OFF"
        time.sleep(1)
  if text[6]=='1':
        GPIO.output(6,1)
        print "Motor2 ON"
        time.sleep(1)
  else :
        GPIO.output(6,0)
        print"Motor2 OFF"
        time.sleep(1)
  
  
  i1 = GPIO.input(7)
  if i1 == 0:
	print "fire detect"
        
	GPIO.output(buzzer, 1)
	B="firedetect"
      
	time.sleep(delay)
  elif i1 == 1:
	print "fire not detect"
        #GPIO.output(relay, 0)	
	GPIO.output(buzzer, 0)
	B="FireNotDetect"
        
	time.sleep(delay)	
 
 
  gas_level = ReadChannel(gas_channel)
  G = int(gas_level/5)
  
  if G > 100:
    print "Gas Lekage: %d "%(G)
    GPIO.output(buzzer, 1)
    GPIO.output(13,1)
  elif G <99:
    print "Gas not Leake: %d "%(G)
    GPIO.output(buzzer, 0)
    GPIO.output(13,0)
  
  otp1=123
    

  cnt =0
  i=0
  k=0
  #if flag1 == 0:
  if GPIO.input(25) == False:
                
                status = 1
                  
                if status == 1:
                        print "Pres otp"
                        while  flag ==1 :
                              #if flag == 1 :
                              if (GPIO.input(21) == False):
                                  while (GPIO.input(21) ==False):
                                      i += 1

                                  cnt=(cnt*10)+1
                                      
                                

                                  
                              if (GPIO.input(20) == False):
                                  while (GPIO.input(20) ==False):
                                      
                                      i += 1  
                                  cnt=(cnt*10)+2

                              if (GPIO.input(16) == False):
                                  while (GPIO.input(16) ==False):
                                       i += 1
                                      
                                  cnt=(cnt*10)+3
                              print cnt
                              
                              time.sleep(1)
                              if cnt >=100:
                                  
                                  
                                  if otp1 == cnt:
                                      print "Pass Ok"
                                      #kill -s otp1
                                      GPIO.output(6,1)
                                      time.sleep(delay)
                                      time.sleep(delay)
                                      GPIO.output(6,0)
                                      flag=0

                                  else:
                                      print "password not match"
                                      k +=1
                                      if k >=3:
                                          print "locked"
                                          os.system('sudo python /home/pi/MagPi/gmail1.py')
                                          
                                          flag=0
                                          
                                      cnt=0
                                  
        

  
  
  
  # Wait before repeating loop
  time.sleep(delay)

