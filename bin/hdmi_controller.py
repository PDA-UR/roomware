#!/usr/bin/python3
# -*- coding: utf-8 -*-

import django
from bin import hdmi_switch

class HdmiController():

	def __init__(self):
		super().__init__()
		self.hdmiSwitch = hdmi_switch.hdmiSwitch()
		self.input = '0'
		self.output = '0'
	
	@property
	def setInput(self):
		return self.input
	
	@setInput.setter	
	def setInput(self, input):
		self.input = input
	
	@property
	def setOutput(self):
		return self.output
	
	@setOutput.setter
	def setOutput(self, output):
		self.output = output
		
	def toggleConnection(self):
		if self.input != '0' and self.output != '0':
			connection = self.hdmiSwitch.outputConnections(self.output)
			if self.input == connection:
				self.hdmiSwitch.switchOff(self.output)
			else:
				self.hdmiSwitch.connect(self.input, self.output)
				
	#def switchStatusDevices():
		
	
		
	
