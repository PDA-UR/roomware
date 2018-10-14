#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial as ser
import time
from configparser import ConfigParser
import os

# hdmi switch for managing the different hdmi devices
class HdmiSwitch():

    def __init__(self):
        super().__init__()
        os.chdir('/home/roomuser/Roomware/roomware')
        config = ConfigParser()
        config.read('config.ini')
        self.serial = ser.Serial(config.get('hdmi_switch', 'usb'))
        self.serial.baudrate = config.getint('hdmi_switch', 'baudrate')
        self.serial.bytesize = ser.EIGHTBITS
        self.serial.parity = ser.PARITY_NONE
        self.serial.stopbits = ser.STOPBITS_ONE
        self.serial.timeout = config.getfloat('hdmi_switch', 'timeout')
        self.read_size_short = config.getint('hdmi_switch', 'read_size_short')
        self.read_size_long = config.getint('hdmi_switch', 'read_size_long')
        self.coding = config.get('hdmi_switch', 'coding')
        self.status_connection = bytes.fromhex(config.get('hdmi_switch', 'status_connection'))
        self.connected_inputs = bytes.fromhex(config.get('hdmi_switch', 'connected_inputs'))
        self.connected_outputs = bytes.fromhex(config.get('hdmi_switch', 'connected_outputs'))
        self.bytes_status = config.get('hdmi_switch', 'bytes_status')
        self.bytes_point = config.get('hdmi_switch', 'bytes_point')
        self.bytes_connect = config.get('hdmi_switch', 'bytes_connect')
        self.bytes_switch_off = config.get('hdmi_switch', 'bytes_switch_off')
        self.bytes_switch_on = config.get('hdmi_switch', 'bytes_switch_on')
        self.connection_off = config.get('hdmi_switch', 'connection_off')
        self.query_connection_null = config.get('hdmi_switch', 'query_connection_null')
        self.query_connection_four = config.getint('hdmi_switch', 'query_connection_four')
        self.query_connection_five = config.getint('hdmi_switch', 'query_connection_five')
        self.start_read = config.getint('hdmi_switch', 'start_read')
        self.midpoint_read = config.getint('hdmi_switch', 'midpoint_read')
        self.end_read = config.getint('hdmi_switch', 'end_read')
        self.available_connection = config.get('hdmi_switch', 'available_connection')
        self.counter = config.getint('hdmi_switch', 'counter')
        self.sleep = config.getint('hdmi_switch', 'sleep')
		
	# gets connections of the input to the output devices
    def status(self):
        self.serial.write(self.status_connection)
        status_feedback = self.serial.read(size=self.read_size_short)
        status_feedback = status_feedback.decode(self.coding)
	
	# shows all connections of a given output
    def output_connections(self, output):
        output_connection = bytes(self.bytes_status + output + self.bytes_point, encoding=self.coding)
        self.serial.write(output_connection)
        connection_feedback = self.serial.read(size=self.read_size_short)
        connection_feedback = connection_feedback.decode(self.coding)
        connection_feedback = self.get_connection(connection_feedback)
        return connection_feedback
		
    def get_connection(self, connection_feedback):
        connection = connection_feedback
        if self.connection_off in connection:
	        connection = self.query_connection_null
        else:
	        if connection_feedback[self.query_connection_four] == self.query_connection_null:
		        connection = connection_feedback[self.query_connection_five]
	        else:
		        connection = connection_feedback[self.query_connection_four]
        return connection
	
	# gives a feedback where hardware is plugged in to inputs
    def status_in(self):
        self.serial.write(self.connected_inputs)
        statusIn_feedback = self.serial.read(size=self.read_size_long)
        statusIn_feedback = statusIn_feedback.decode(self.coding)
        inputDevices = self.getInOutDevices(statusIn_feedback)
        return inputDevices
		
	# gives a feedback where hardware is plugged in to outputs
    def status_out(self):
        self.serial.write(self.connected_outputs)
        statusOut_feedback = self.serial.read(size=self.read_size_long)
        statusOut_feedback = statusOut_feedback.decode(self.coding)
        outputDevices = self.getInOutDevices(statusOut_feedback)
        return outputDevices
		
	# filters the plugged devices
    def get_in_out_devices(self, status):
        newStatus = (status[self.start_read:self.midpoint_read] + status[self.end_read:]).replace(' ', '')
        devices = []
        for i in range(len(newStatus)):
	        if newStatus[i] == self.available_connection:
		        devices.append(i+self.counter)
        return devices
		
	# connects an input to an output
    def connect(self, inputs, output):
        connection = bytes(inputs + self.bytes_connect + output + self.bytes_point, encoding=self.coding)
        self.serial.write(connection)
        time.sleep(self.sleep)
		
	# switches off an output
    def switch_off(self, output):
        connection = bytes(output + self.bytes_switch_off, encoding=self.coding)
        self.serial.write(connection)
		
	# switches on an output
    def switch_on(self, output):
        connection = bytes(output + self.bytes_switch_on, encoding=self.coding)
        self.serial.write(connection)
