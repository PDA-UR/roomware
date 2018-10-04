#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial as ser
import subprocess
import time

class USBSwitch():

	def __init__(self):
		super().__init__()
		self.serial = ser.Serial('/dev/ttyUSB1')
		self.serial.baudrate = 9600
		self.serial.bytesize = 8
		self.serial.parity = 'N'
		self.serial.stopbits = 1
		self.number_of_hub = 1
		self.switch = "Realtek Semiconductor Corp. RTL 8153 USB 3.0 hub with gigabit ethernet"
        
	def changeHub(self):
		input_on = b'\x01'
		self.serial.write(input_on)
		time.sleep(1)
		
		
	def setNumberSwitch(self):
		if self.number_of_hub == 4:
			self.number_of_hub = 1
		else:
			self.number_of_hub += 1
		
	def checkUSB(self):
		output = subprocess.check_output("lsusb")
		if str(output).find(self.switch) != -1:
			return True
		else: 
			return False
			
	def findUSBSwitch(self):
		find_connection = self.checkUSB()
		while find_connection is False:
			self.changeHub()
			time.sleep(1)
			find_connection = self.checkUSB()
			
		self.number_of_hub = 1
		
	
#USBSwitch().changeHub()		
USBSwitch().findUSBSwitch()
	
	
