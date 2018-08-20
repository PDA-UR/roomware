#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial 
import sispm

id = '01:ff:ff:ff:ff'

devices = sispm.connect()

dev = None
for d in devices:
	if sispm.getid(d) == id:
		dev = d

sispm.switchoff(dev, 3)
