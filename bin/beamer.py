#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial as ser

class Beamer():

	def __init__(self):
		super().__init__()
		self.serial = ser.Serial('/dev/ttyUSB0')
		self.serial.baudrate = 19200
		self.serial.bytesize = 8
		self.serial.parity = 'N'
		self.serial.stopbits = 1
		
	
	def on(self):
		input_on = b'\xbe\xef\x10\x05\x00\xc6\xff\x11\x11\x01\x00\x01'
		self.serial.write(input_on)
		
	def off(self):
		input_off = b'\xbe\xef\x10\x05\x00\x0c\x3e\x11\x11\x01\x00\x18'
		self.serial.write(input_off)
	
	
