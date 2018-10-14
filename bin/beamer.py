#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial as ser
from bin import powerstrip as power
import time
from configparser import ConfigParser
import os

class Beamer():

    def __init__(self, usb, baudrate, bytesize, parity, stopbits, timeout):
        super().__init__()
        os.chdir('/home/roomuser/Roomware/roomware')
        config = ConfigParser()
        config.read('config.ini')
        self.serial = ser.Serial(usb)
        self.serial.baudrate = baudrate
        self.serial.bytesize = bytesize
        self.serial.parity = parity
        self.serial.stopbits = stopbits
        self.serial.timeout = timeout
        self.sleep_on = config.getint('beamer', 'sleep_on')
        self.sleep_off = config.getint('beamer', 'sleep_off')
        self.state_size = config.getint('beamer', 'state_size')
        self.byteorder = config.get('beamer', 'byteorder')
        self.length_on = config.get('beamer', 'length_on')
        self.length_off = config.get('beamer', 'length_off')
        self.bytelength = config.getint('beamer', 'bytelength')
    
    #switch on beamer with given input hex code    
    def on(self, input_on):
        time.sleep(self.sleep_on)
        self.serial.write(input_on)
        time.sleep(self.sleep_on)
	
    #switch off beamer with given input hex code	
    def off(self, input_off):
        time.sleep(self.sleep_on)
        self.serial.write(input_off)
        time.sleep(self.sleep_off)

    #reads in the input hex code for status query and switch on or off in dependence 
    #of the current state 
    def change_state(self, input_change_state, input_on, input_off):
        time.sleep(self.sleep_on)
        self.serial.write(input_change_state)
        s = self.serial.read(size=self.state_size)
        s_hex = hex(int.from_bytes(s, byteorder=self.byteorder))
        status = s_hex[self.bytelength]
        if str(status) == self.length_on:
            self.on(input_on)
        if str(status) == self.length_off:
            self.off(input_off)		
	
