#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial as ser
import subprocess
import time
from configparser import ConfigParser
import os


# usb switch for managing the usb devices (cameras)
class USBSwitch():

    def __init__(self):
        super().__init__()
        os.chdir('/home/roomuser/Roomware/roomware')
        config = ConfigParser()
        config.read('config.ini')
        self.serial = ser.Serial(config.get('usb_switch', 'usb'))
        self.serial.baudrate = config.getint('usb_switch', 'baudrate')
        self.serial.bytesize = config.getint('usb_switch', 'bytesize')
        self.serial.parity = config.get('usb_switch', 'parity')
        self.serial.stopbits = config.getint('usb_switch', 'stopbits')
        self.number_of_hub = config.getint('usb_switch', 'number_of_hub')
        self.switch = config.get('usb_switch', 'switch')
        self.input_on = bytes.fromhex(config.get('usb_switch', 'input_on'))
        self.sleep_hub = config.getint('usb_switch', 'sleep_hub')
        self.number_of_hubs = config.getint('usb_switch', 'number_of_hubs')
        self.first_hub = config.getint('usb_switch', 'first_hub')
        self.check_usb_name = config.get('usb_switch', 'check_usb_name')
        self.no_usb_available = config.getint('usb_switch', 'no_usb_available')
        self.to_previous_hub = config.getint('usb_switch', 'to_previous_hub')

    # changes the switch to the next hub
    def change_hub(self):
        self.serial.write(b'\x01')
        self.set_number_switch()
        time.sleep(self.sleep_hub)

    # changes the switch to the previous hub
    def change_to_previous_hub(self):
        for i in range(self.to_previous_hub):
            self.serial.write(b'\x01')
            self.set_number_switch()
            time.sleep(self.sleep_hub)

    # changes the switch to a specific given hub number
    def change_to_number(self, hub):    
        if hub < self.number_of_hub:
            for i in range(abs(self.number_of_hub - hub)):
                self.change_to_previous_hub()
        else:
            for i in range(abs(self.number_of_hub - hub)):
                self.serial.write(b'\x01')
                self.set_number_switch()
                time.sleep(self.sleep_hub)

    # sets the number of the hub which is currently used
    def set_number_switch(self):
        if self.number_of_hub == self.number_of_hubs:
            self.number_of_hub = self.first_hub
        else:
            self.number_of_hub += self.first_hub

    # checks if the input devices are set to the roomie (output 1)
    def check_usb(self):
        output = subprocess.check_output(self.check_usb_name)
        if str(output).find(self.switch) != self.no_usb_available:
            return True
        else:
            return False

    # sets the output to the roomie (output 1)
    def find_usb_switch(self):
        find_connection = self.check_usb()
        while find_connection is False:
            self.change_hub()
            find_connection = self.check_usb()

        self.number_of_hub = self.first_hub
