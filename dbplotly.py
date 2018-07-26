#!/usr/bin/python

import datetime
import MySQLdb
import pandas as pd
import plotly.plotly as py
from plotly.graph_objs import *

py.sign_in('cduff29','mdrk6hklyg')

user_id = "logger"
password = "procarbine"
host = "localhost"
database = "temperatures"

# Open database connection
db = MySQLdb.connect(host,user_id, password, database)

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to gather data from past 24 hours
sql = "SELECT * FROM temperaturedata WHERE dateandtime >= now() - INTERVAL 1 DAY"

try:
   # Execute the SQL command
   cursor.execute(sql)
   rows = cursor.fetchall()
except:
   print "Error: unable to fecth data"

#convert tuple of tuples to DataFrame object
df = pd.DataFrame( [[ij for ij in i] for i in rows] )
df.rename(columns={0: 'Date and Time', 1: 'Fermentor', 2: 'Surface', 3: 'Room'}, inplace=True, parse_dates=True);

trace1 = Scatter(
     x=df['Date and Time'],
     y=df['Fermentor'],
     name='Fementor Temperature'
)

trace2 = Scatter(
     x=df['Date and Time'],
     y=df['Surface'],
     name='Surface Temperature'
)

trace3 = Scatter(
     x=df['Date and Time'],
     y=df['Room'],
     name='Room Temperature'
)

layout = Layout(
     xaxis=XAxis( title='Date and Time' ),
     yaxis=YAxis( type='log', title='Temperature' ),
     showlegend=True
)

data = Data([trace1, trace2, trace3])

py.plot(data, filename='Time vs Temperature')
 
# disconnect from server
db.close()
