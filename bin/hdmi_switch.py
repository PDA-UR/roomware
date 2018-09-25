#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial as ser
import time

# hdmi switch for managing the different hdmi devices
class hdmiSwitch():

	def __init__(self):
		super().__init__()
		self.serial = ser.Serial('/dev/ttyUSB0')
		self.serial.baudrate = 9600
		self.serial.bytesize = 8
		self.serial.parity = 'N'
		self.serial.stopbits = 1
		self.serial.timeout = 5
		
	# gets connections of the input to the output devices
	def status(self):
		status_connection = b'%9975.'
		self.serial.write(status_connection)
		status_feedback = self.serial.read(size=70)
		#print("status", status_feedback)
		status_feedback = status_feedback.decode('utf-8')
	
	# shows all connections of a given output
	def outputConnections(self, output):
		output_connections = bytes('Status' + output + '.', encoding='utf-8')
		self.serial.write(output_connections)
		connection_feedback = self.serial.read(size=70)
		connection_feedback = connection_feedback.decode('utf-8')
		connection_feedback = self.getConnection(connection_feedback)
		return connection_feedback
		
	def getConnection(self, connection_feedback):
		connection = connection_feedback
		if 'OFF' in connection:
			connection = '0'
		else:
			if connection_feedback[4] == '0':
				connection = connection_feedback[5]
			else:
				connection = connection_feedback[4]
		return connection
	
	# gives a feedback where hardware is plugged in to inputs
	def statusIn(self):
		statusIn_connection = b'%9971.'
		self.serial.write(statusIn_connection)
		statusIn_feedback = self.serial.read(size=80)
		statusIn_feedback = statusIn_feedback.decode('utf-8')
		inputDevices = self.getInOutDevices(statusIn_feedback)
		print("inputDevices: ", inputDevices)
		#return inputDevices
		
	# gives a feedback where hardware is plugged in to outputs
	def statusOut(self):
		statusOut_connection = b'%9972.'
		self.serial.write(statusOut_connection)
		statusOut_feedback = self.serial.read(size=80)
		statusOut_feedback = statusOut_feedback.decode('utf-8')
		outputDevices = self.getInOutDevices(statusOut_feedback)
		print("outputDevices: ", outputDevices)
		#return outputDevices
		
	# filters the plugged devices
	def getInOutDevices(self, status):
		newStatus = (status[27:34] + status[64:]).replace(' ', '')
		devices = []
		for i in range(len(newStatus)):
			if newStatus[i] == 'Y':
				devices.append(i+1)
		return devices
		
	# connects an input to an output
	def connect(self, input, output):
		connection = bytes(input + 'V' + output + '.', encoding='utf-8')
		self.serial.write(connection)
		time.sleep(3)
		
	# switches off an output
	def switchOff(self, output):
		connection = bytes(output + '$.', encoding='utf-8')
		self.serial.write(connection)
		
	# switches on an output
	def switchOn(self, output):
		connection = bytes(output + '@.', encoding='utf-8')
		self.serial.write(connection)
		
#hdmiSwitch().status()
#hdmiSwitch().connect('1', '1')
#hdmiSwitch().status()
#hdmiSwitch().switchOff()
#hdmiSwitch().switchOn()
#hdmiSwitch().status()
#hdmiSwitch().statusIn()
#hdmiSwitch().statusOut()
