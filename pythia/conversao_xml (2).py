# -*- coding: utf-8 -*-
"""Conversao_XML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wdCHV8omQ54CoAnsNP1jAu7ZH0yXO9Ja
"""

import csv
from datetime import datetime


input_filename = 'arquivo_dados.csv'

output_filename = 'output.xml'


#importing the database and reading the data
f = open(input_filename)
csv_f = csv.reader(f)

#converting all the data into a list of lists
#(each inner list is a row, and each element is a parameter measured)
data = []
for row in csv_f: 
   data.append(row)
f.close()

#Remove the labels
data = data[1:]

#Converting the Timestamps into time deltas
counter = 0
for n in data:
  if counter == 0:
    first_timeStamp = datetime.strptime(n[0], "%Y.%m.%d_%H.%M.%S")
    n[0] = first_timeStamp - first_timeStamp
    n[0] = n[0].total_seconds()
  else:
    timeStamp = datetime.strptime(n[0], "%Y.%m.%d_%H.%M.%S")
    n[0] = timeStamp - first_timeStamp
    n[0] = n[0].total_seconds()
  counter = counter + 1

#Correcting the PingAVG variable
counter = 0
last_ping = False
for n in data:
  if n[15] != '-':
    last_ping = True
  elif n[15] == '-' and last_ping == True:
    auxiliar_data = data[:counter]
    for n2 in auxiliar_data[::-1]:
      if n[5] == n2[5] and n2[15] != '-':
        n[15] = n2[15]
        break
  counter = counter + 1

#Transforming the '-' into '0'
for n in data:
  if n[15] == '-':
    n[15] = 0

#print (data)

#This part of the code writes the initial information for the database and tests
#Not in a loop for every line of the database
with open('output.xml','w') as f:
  f.write("""<?xml version="1.0"?>
<experiment>

  <!-- UEs -->
  <!-- The file ueA_positions.csv represents a walk from 
  Triumph's arc to Tour Eiffel in 40 minutes -->
  <ue name="ueA" positions_file="example/ue1_positions.csv">
    <ue_app name="client1" image="simple_client" command="simple_server:8080 1"/>
  </ue>

  <!-- MEC Hosts -->
  <mec_host name="mecA" memmory="1" cpu="2"/>
  <mec_host name="mecB" memmory="1" cpu="2"/>

  <!-- MEC Apps -->
  <mec_app name="server1" image="simple_server" ip="172.21.0.3" command=""/>\n""")

#converting the data list, row by row, into a xml file
def convert_row(row):

  #For latency, the variable used was PingAVG
  return """
  <link ue="ueA" mec_host="%s" latency="%s" upload="%sMbps" download="%sMbps" time="%s"/>""" % (row[5],\
    row[15], row[13], row[12], row[0])

#Since this function uses append, it's important to not use it seperately if
#the named file already exist in the Desktop
with open(output_filename,'a') as f:
  f.write('\n'.join([convert_row(row) for row in data]))