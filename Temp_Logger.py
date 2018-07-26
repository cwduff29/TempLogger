#!/usr/bin/python2
#coding=utf-8
import time
import datetime
from datetime import timedelta
import subprocess
import os
import re
import sys
import MySQLdb
from ConfigParser import ConfigParser

#Function for reading sensor data
def sensorReadings(location, sensor):
 #Get file path for sensor reading script
 tempPath = "/home/pi/TempLogger/Temp_Sensor_Read.py"
 
 Rrun system command
 sensorReadings = os.popen('sudo python ' + tempPath + " " + sensor + " " +  location).read()
 temperature = re.findall(r"Temp=(\d+.\d+)", sensorReadings)[0]
 intTemp = float(temperature)
 return intTemp

#Function to get configurations
def getConfigurations():	
 #Get configuration file path
 path = os.path.dirname(os.path.realpath(sys.argv[0]))
 configurationFile = path + '/config.ini'

 #Load configurations
 config = ConfigParser()
 config.read(configurationFile)
      		
 return config
 
# helper function for database actions. Handles select, insert and sqldumpings. Update te be added later
def databaseHelper(sqlCommand, sqloperation):	
 configurations = getConfigurations()
	
 host = configurations.get('mysql', 'host')
 user = configurations.get('mysql', 'user')
 dbpassword = configurations.get('mysql', 'password')
 database = configurations.get('mysql', 'database')
 backuppath = "/home/pi/TempLogger/Backup/"
  
 data = ""
	
 db = MySQLdb.connect(host,user,dbpassword,database)
 cursor=db.cursor()

 if sqloperation == "Select":
  try:
   cursor.execute(sqlCommand)
   data = cursor.fetchall()
  except:
   db.rollback()

 elif sqloperation == "Insert":
  try:
   cursor.execute(sqlCommand)
   db.commit()
  except:
   db.rollback()
   sys.exit(0)

 elif sqloperation == "Backup":  
  # Getting current datetime to create seprate backup folder like "12012013-071334".
  day = datetime.date.today().strftime("%Y-%m-%d")
  backupbathoftheday = backuppath + date

  # Checking if backup folder already exists or not. If not exists will create it.
  if not os.path.exists(backupbathoftheday):
   os.makedirs(backupbathoftheday)

  # Dump database
  db = database
  dumpcmd = "mysqldump -u " + user + " -p" + dbpassword + " " + database + " > " + backupbathoftheday + "/" + db + ".sql"
  os.system(dumpcmd)
 
 return data
	
def main():
 #Get configurations
 configurations = getConfigurations()
 sensorType = configurations.get('sensors', 'sensorType')
 Location1 = configurations.get('sensors', 'sensorLocation1')
 Location2 = configurations.get('sensors', 'sensorLocation2')
 Location3 = configurations.get('sensors', 'sensorLocation3')
 Sensor1 = configurations.get('sensors', 'sensorName1')
 Sensor2 = configurations.get('sensors', 'sensorName1')
 Sensor3 = configurations.get('sensors', 'sensorName1')
 backupEnabled = configurations.get('sqlBackupDump', 'backupDumpEnabled')
 backupHour = configurations.get('sqlBackupDump', 'backupHour')
 
 currentTime = datetime.datetime.now()
 d = datetime.date.weekday(datetime.datetime.now())
 h = datetime.datetime.now()

 # check if it is 5 o clock. If yes, take sql dump as backup
 if backupEnabled == "Y" or backupEnabled == "y":
  if h.hour == int(backupHour):
   databaseHelper("","Backup")

 sensor1temperature = sensorReadings(sensorName1, sensorType)
 sensor2temperature = sensorReadings(sensorName2, sensorType)
 sensor3temperature = sensorReadings(sensorName3, sensorType)

 # insert values to db
 try:
  sqlCommand = "INSERT INTO temperaturedata SET dateandtime='%s', temperature1='%s', temperature2='%s', temperature3='%s'" % (currentTime,sensor1temperature,sensor2temperature,sensor3temperature)
  databaseHelper(sqlCommand,"Insert")
  
except:
 sys.exit(0)
if __name__ == "__main__":
 main()
