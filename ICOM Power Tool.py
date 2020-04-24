#!/usr/bin/env python3

# Author: AI0J (Eric Dropps) - eric@ai0j.radio
import binascii
import re
import serial
import sys
import time

## Settings
COM_PORT = 'COM3' # What COM port is the radio connected to?
BAUD_RATE = 19200 # This Does NOT have to match your CAT software setting.
RADIO_ID = b'\x95' # ID here is 94, default for the IC-7300  \x means use HEX value
# Known radio ID's
# IC-7300: 94
# IC-7100: 88
# ID-5100: 8C

BAUD_RATE_COMMAND = b'\xFE'
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
baud_rate_setting = bytearray()
for x in range(0,BAUD_RATE_COMMAND_COUNT[BAUD_RATE]):
  baud_rate_setting.extend(b'\xFE')

# Assemble power commands
power_on_command = bytearray()
power_on_command.extend(baud_rate_setting)
power_on_command.extend(b'\xFE\xFE')
power_on_command.extend(RADIO_ID)
power_on_command.extend(b'\xE0\x18\x01\xFD')

power_off_command = bytearray()
power_off_command.extend(b'\xFE\xFE')
power_off_command.extend(RADIO_ID)
power_off_command.extend(b'\xE0\x18\x00\xFD')

# Init Serial Port
ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=15) 

# Send the command requested
if len(sys.argv) > 1:
  if sys.argv[1] == "--off":
    print("Powering off")
    ser.write(power_off_command)
  else:
    print("Unknown argument %s" % sys.argv[1])
    sys.exit(1)
else:
  print("Powering on")
  ser.write(power_on_command)

# Wait for and decode response
time.sleep(1)
bytes_returned = ser.inWaiting()
response = binascii.hexlify(ser.read(bytes_returned))

# Find response from radio in returned data
result = re.search(r"fefee0..(f[db])fd",response.decode(encoding='utf-8'))

if result == None:
  print("No valid response from radio received.  Check settings for COM port, radio ID, and baud rate.")
elif (result.group(1) == "fb"):
  print("Radio accepted power command.")
elif (result.group(1) == "fa"):
  print("Radio returned an error.")
  print("Received %i bytes" % bytes_returned)
  print("Returned data: %s" % response)
else:
  print( "Unexpected response from radio/serial port: %s" % response)
  time.sleep(15)
time.sleep(5)