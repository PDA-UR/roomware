#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial as ser
import time

class hdmiSwitch():

	def __init__(self):
		super().__init__()
		self.serial = ser.Serial('/dev/ttyUSB0')
		self.serial.baudrate = 9600
		self.serial.bytesize = 8
		self.serial.parity = 'N'
		self.serial.stopbits = 1
		self.serial.timeout = 5
		
	def status(self):
		status_connection = b'Status.'
		self.serial.write(status_connection)
		status_feedback = self.serial.read(size=300)
		print(status_feedback)
		
	def connect(self):
		connection = b'4V1.'
		self.serial.write(connection)
		time.sleep(3)
		connection = b'2V5.'
		self.serial.write(connection)
		
	def switchOff(self):
		connection = b'2$.'
		self.serial.write(connection)
		
#hdmiSwitch().status()
#hdmiSwitch().connect()
#hdmiSwitch().status()
hdmiSwitch().switchOff()
