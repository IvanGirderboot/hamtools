#!/usr/bin/env python

# Author: AI0J (Eric Dropps) - eric@ai0j.name
import binascii
import serial
import time


## Settings
COM_PORT = 'COM3' # What COM port is the radio connected to?
BAUD_RATE = 19200 # This Does NOT have to match your CAT software setting.
RADIO_ID = '\x88' # ID here is 88, default for the IC-7100  \x means use HEX value
# Known radio ID's
# IC-7300: 94
# IC-7100: 88
# ID-5100: 8C

BAUD_RATE_COMMAND = '\xFE'
BAUD_RATE_COMMAND_COUNT = { 
  115200: 150,
  57600: 75,
  38400: 50,
  19200: 25,
  9600: 26,
  4800: 7,
  1200: 3,
  300: 2 
  }

## DO NOT EDIT BELOW

# setup variable for pre-preamble based on selected baud rate.
baud_rate_setting = ''
for x in range(0,BAUD_RATE_COMMAND_COUNT[BAUD_RATE]):
  baud_rate_setting += '\xFE'

# Assemble power on command
power_on_command = baud_rate_setting + '\xFE\xFE' + RADIO_ID + '\xE0\x18\x01\xFD'

# Init Serial Port
ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=15) 

# Send the command
ser.write(power_on_command)

# Wait for and decode response
time.sleep(1)
bytes_returned = ser.inWaiting()
response = binascii.hexlify(ser.read(bytes_returned))

# Determine the outcome
if bytes_returned != BAUD_RATE_COMMAND_COUNT[BAUD_RATE] + 13:
  print "Unexpected amount of return data. Check connections and try again"
  print "Recieved %i bytes" % bytes_returned 
  print "Returned data: %s" % response
  quit()

if (response[-4:-2] == "fb"):
  print "Radio accepted power on command."
elif (response[-4:-2] == "fa"):
  print "Radio returned an error."
else:
  print "Unexpeted response from radio/serial port: %s" % response
  time.sleep(15)
time.sleep(5)