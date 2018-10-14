#!/usr/bin/python3
# -*- coding: utf-8 -*-

import django
from bin import hdmi_switch
import os
from configparser import ConfigParser

class HdmiController():

    def __init__(self):
        super().__init__()
        os.chdir('/home/roomuser/Roomware/roomware')
        self.config = ConfigParser()
        self.config.read('config.ini')
        self.hdmi_switch = hdmi_switch.HdmiSwitch()
        self.input = self.config.get('hdmi_controller', 'null')
        self.output = self.config.get('hdmi_controller', 'null')
	
    @property
    def set_input(self):
        return self.input
	
    @set_input.setter	
    def set_input(self, inputs):
        self.input = inputs
	
    @property
    def set_output(self):
        return self.output
	
    @set_output.setter
    def set_output(self, output):
        self.output = output
		
    def toggle_connection(self):
        if self.input != self.config.get('hdmi_controller', 'null') and self.output != self.config.get('hdmi_controller', 'null'):
            connection = self.hdmi_switch.output_connections(self.output)
            if self.input == connection:
                self.hdmi_switch.switch_off(self.output)
            else:
                self.hdmi_switch.connect(self.input, self.output)
