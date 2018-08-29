#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial 
import sispm

class Powerstrip():
    def __init__(self):
        super().__init__()
        self.id = '01:ff:ff:ff:ff'
        self.devices = sispm.connect()
        self.dev = None
        self.power_beamer = 2
        
    def switchOn(self):
        for d in self.devices:
            if sispm.getid(d) == self.id:
                self.dev = d
        sispm.switchon(self.dev, self.power_beamer)
        
    def switchOff(self):
        for d in self.devices:
            if sispm.getid(d) == self.id:
                self.dev = d
        sispm.switchoff(self.dev, self.power_beamer)
