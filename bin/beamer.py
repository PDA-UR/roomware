#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial as ser
from bin import powerstrip as power
import time

class Beamer():

	def __init__(self):
		super().__init__()
		self.serial = ser.Serial('/dev/ttyUSB0')
		self.serial.baudrate = 19200
		self.serial.bytesize = 8
		self.serial.parity = 'N'
		self.serial.stopbits = 1
		self.serial.timeout = 5
		self.powerStrip = power.Powerstrip()
        
	def on(self):
		self.powerStrip.switchOn()
		time.sleep(5)
		input_on = b'\xbe\xef\x10\x05\x00\xc6\xff\x11\x11\x01\x00\x01'
		self.serial.write(input_on)
		
	def off(self):
		input_off = b'\xbe\xef\x10\x05\x00\x0c\x3e\x11\x11\x01\x00\x18'
		self.serial.write(input_off)
		time.sleep(15)
		self.powerStrip.switchOff()
	
	def changeState(self):
		self.serial.write(b'\xbe\xef\x10\x05\x00\x46\x7e\x11\x11\x01\x00\xff')
		s = self.serial.read(size=3)
		s_hex = hex(int.from_bytes(s, byteorder='little'))
		status = s_hex[2]
		if str(status) == '0':
			self.on()
		if str(status) == '3':
			self.off()		
	
