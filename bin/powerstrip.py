#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sispm
from configparser import ConfigParser
import os
import subprocess
import usb.core

class Powerstrip():
    def __init__(self, device_room):
        super().__init__()
        os.chdir('/home/roomuser/Roomware/roomware')
        config = ConfigParser()
        config.read('config.ini')
        self.devices = sispm.connect()
        self.device_room = device_room
        self.device_id = config.get('powerstrip', 'device_id')
        self.powerstrip_length = config.getint('powerstrip', 'powerstrip_length')
        self.first_socket = config.getint('powerstrip', 'first_socket')
        self.powerstrips_rooms = {}
        if len(self.devices) > 1:
            self.powerstrips_rooms = {"1": self.devices[0], "2": self.devices[1]}
       
    # switches a given socket of the powerstrip on
    def switch_on(self, socket):
        try:
            if sispm.getid(self.powerstrips_rooms[str(self.device_room)]) == self.device_id:
                sispm.switchon(self.powerstrips_rooms[str(self.device_room)], socket)
        except Exception as e:
            print('Powerstrip().switch_on()', e)

    # switches a given socket of the powerstrip off
    def switch_off(self, socket):
        try:
            for d in self.devices:
                if sispm.getid(self.powerstrips_rooms[str(self.device_room)]) == self.device_id:
                    sispm.switchoff(self.powerstrips_rooms[str(self.device_room)], socket)
        except Exception as e:
            print('Powerstrip().switch_off()', e)

    # switches all sockets of the powerstrip on
    def switch_all_on(self):
        try:
            if sispm.getid(self.powerstrips_rooms[str(self.device_room)]) == self.device_id:
                for i in range(self.powerstrip_length):
                    socket = self.first_socket + i
                    sispm.switchon(self.powerstrips_rooms[str(self.device_room)], socket)
        except Exception as e:
            print('Powerstrip().switch_all_on()', e)

    # switches all sockets of the powerstrip off
    def switch_all_off(self):
        try:
            if sispm.getid(self.powerstrips_rooms[str(self.device_room)]) == self.device_id:
                for i in range(self.powerstrip_length):
                    socket = self.first_socket + i
                    sispm.switchoff(self.powerstrips_rooms[str(self.device_room)], socket)
        except Exception as e:
            print('Powerstrip().switch_all_off()', e)

    # gives the status whether the given socket of the powerstrip is on or off
    def status(self, socket):
        status = sispm.getstatus(self.powerstrips_rooms[str(self.device_room)], socket)
        return status

    # gives the status whether all sockets of the powerstrip are on or off
    def status_all(self):
        status = []
        try:
            if sispm.getid(self.powerstrips_rooms[str(self.device_room)]) == self.device_id:
                for i in range(self.powerstrip_length):
                    status.append(sispm.getstatus(self.powerstrips_rooms[str(self.device_room)], i))
                return status
        except Exception as e:
            print('Powerstrip().status_all()', e)
            return None

