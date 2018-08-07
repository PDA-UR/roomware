#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial

serial = serial.Serial('/dev/ttyUSB0')
serial.baudrate = 19200
serial.bytesize = 8
serial.parity = 'N'
serial.stopbits = 1

input_on = b'\xbe\xef\x10\x05\x00\xc6\xff\x11\x11\x01\x00\x01'
serial.write(input_on)
