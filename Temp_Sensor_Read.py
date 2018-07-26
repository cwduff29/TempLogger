#!/usr/bin/python 
# Copyright (c) 2014 Adafruit Industries 
# Original Author: Tony DiCola 
# Modified By: Chris Duff


# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions: 
 
 
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software. 

import os
import time
import sys
import Adafruit_DHT

#Read raw output from modprobe
def read_temp_raw():
 f = open(device_file, 'r')
 lines = f.readlines()
 f.close()
 return lines

#Get temperature data
def read_temp():
 lines = read_temp_raw()
 
 #Separate number from output
 while lines[0].strip()[-3:] != 'YES':
  time.sleep(0.1)
  lines = read_temp_raw()
 equals_pos = lines[1].find('t=')
 
 #Convert reading to temperature
 if equals_pos != -1:
  temp_string = lines[1][equals_pos+2:]
  temp_c = float(temp_string) / 1000.0
  temp_f = temp_c * 9.0 / 5.0 + 32.0
  
 return temp_f	

# Parse command line parameters.
sensor_args = { 'DHT11': Adafruit_DHT.DHT11,
				'DHT22': Adafruit_DHT.DHT22,
				'AM2302': Adafruit_DHT.AM2302,
				'DS18B20': 'DS18B20'}
			
dht_sensors = { 'DHT11',
				'DHT22',
				'AM2302'}

if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
 sensor = sensor_args[sys.argv[1]]
 location = sys.argv[2]
else:
 print('usage: sudo ./Temp_Sensor_Read.py [11|22|2302] GPIOpin or Sensor Name')
 sys.exit(1)

# Try to grab a AM2302 sensor reading.  Use the read_retry method which will retry up 
# to 15 times to get a sensor reading (waiting 2 seconds between each retry). 
if sys.argv[1] in dht_sensors:	
 humidity, temperature = Adafruit_DHT.read_retry(sensor, location) 
elif sys.argv[1] == 'DS18B20':	 
 #Prepare to get DS18B20 temperature
 os.system('modprobe w1-gpio')
 os.system('modprobe w1-therm')

 base_dir = '/sys/bus/w1/devices/'
 device_folder = base_dir + location
 device_file = device_folder + '/w1_slave'
 temperature = read_temp()
else:	
 print('Error: Sensor not supported by this module')
 sys.exit(1)
 
# Note that sometimes you won't get a reading and the results will be null so try again
if temperature is not None: 
 if sys.argv[1] in dht_sensors:
  #If sensor is DHT, convert to fahrenheit
  temperature = temperature * 9.0/5.0 + 32
  print(' Temp={0:0.1f} F  Humidity={1:0.1f}%'.format(temperature, humidity))
  
 else:
  print(' Temp={0:0.1f} F'.format(temperature))

else:
 print('Failed to get reading. Try again!')
 sys.exit(1)
