#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bin import hdmi_controller
from bin import beamer
from bin import ffmpeg_stream as ffstr
from bin import powerstrip
from bin import usb_switch
from bin import hdmi_switch
from configparser import ConfigParser
import os
import time

class Controller():
    
    def __init__(self):
        super().__init__()
        os.chdir('/home/roomuser/Roomware/roomware')
        self.config = ConfigParser()
        self.config.read('config.ini')

        self.hdmi_controller = hdmi_controller.HdmiController()
        self.hdmi_switch = hdmi_switch.HdmiSwitch()
        self.powerstrip_studio = powerstrip.Powerstrip(1)
        self.powerstrip_labor = powerstrip.Powerstrip(2)
        self.beamer_1 = ""
        self.beamer_2 = ""
        self.beamer_3 = ""        
        self.beamer_4 = ""
        self.beamers = {}
        self.usb_switch = usb_switch.USBSwitch()
        self.usb_switch.find_usb_switch()
        self.get_projectors()
    
    # initializes all connected projectors
    def get_projectors(self):
        sections = self.config.sections()
        count = 1
        for section in sections:
            if str(section).find("beamer") == 0:
                if str(section) != 'beamer':
                    options = self.config.options(section)
                    opt = self.config.get(section, 'baudrate')
                    if opt != "None":
                        if str(section)[6] == "1":
                            self.beamer_1 = beamer.Beamer(self.config.get(section, "usb"), self.config.getint(section, "baudrate"), self.config.getint(section, "bytesize"), self.config.get(section, "parity"), self.config.getint(section, "stopbits"), self.config.getint(section, "timeout"))
                            self.beamers = {"1": "beamer1"}
                        if str(section)[6] == "2":
                            self.beamer_2 = beamer.Beamer(self.config.get(section, "usb"), self.config.getint(section, "baudrate"), self.config.getint(section, "bytesize"), self.config.get(section, "parity"), self.config.getint(section, "stopbits"), self.config.getint(section, "timeout"))
                            self.beamers = {"2": "beamer2"}
                        if str(section)[6] == "3":
                            self.beamer_3 = beamer.Beamer(self.config.get(section, "usb"), self.config.getint(section, "baudrate"), self.config.getint(section, "bytesize"), self.config.get(section, "parity"), self.config.getint(section, "stopbits"), self.config.getint(section, "timeout"))
                            self.beamers = {"3", "beamer3"}
                        if str(section)[6] == "4":
                            self.beamer_4 = beamer.Beamer(self.config.get(section, "usb"), self.config.getint(section, "baudrate"), self.config.getint(section, "bytesize"), self.config.get(section, "parity"), self.config.getint(section, "stopbits"), self.config.getint(section, "timeout"))
                            self.beamers = {"4", "beamer4"}
            

    # control the switch, switch on power and projectors and toggle the connection between output and input
    def control_hdmi_switch(self, inp, output):
        print("in and out", inp, output)
        if int(output) < 3:
            status = self.status_powerstrip_studio()
            if status['beamer_'+output] != 1:
                if output == "1":
                    self.powerstrip_studio.switch_on(1)
                else:
                    self.powerstrip_studio.switch_on(4)
        else:
            print(">=3")
            status = self.status_powerstrip_labor()
            if status['beamer_'+output] != 1:
                print("!=1")
                if output == "3":
                    self.powerstrip_labor.switch_on(4)
                else:
                    print("powerstrip")
                    self.powerstrip_labor.switch_on(1)
        time.sleep(5)
        if int(output) == 1:
            if self.beamer_1 != "":
                self.beamer_1.on(bytes.fromhex(self.config.get("beamer1", "input_on")))
        if int(output) == 2:
            if self.beamer_2 != "":
                self.beamer_2.on(bytes.fromhex(self.config.get("beamer2", "input_on")))
        if int(output) == 3:
            if self.beamer_3 != "":
                self.beamer_3.on(bytes.fromhex(self.config.get("beamer3", "input_on")))
        if int(output) == 4:
            if self.beamer_4 != "":
                print(bytes.fromhex(self.config.get("beamer4", "input_on")))
                self.beamer_4.on(bytes.fromhex(self.config.get("beamer4", "input_on")))
        
        feedback = self.hdmi_switch.output_connections(output)
        if int(feedback) == int(inp):
            time.sleep(2)
            if int(output) == 1:
                if self.beamer_1 != "":
                    self.beamer_1.off(bytes.fromhex(self.config.get("beamer1", "input_off")))
                    self.powerstrip_studio.switch_off(1)
            if int(output) == 2:
                if self.beamer_2 != "":
                    self.beamer_2.off(bytes.fromhex(self.config.get("beamer2", "input_off")))
                    self.powerstrip_studio.switch_off(4)
            if int(output) == 3:
                if self.beamer_3 != "":
                    self.beamer_3.off(bytes.fromhex(self.config.get("beamer3", "input_off")))
                    self.powerstrip_labor.switch_off(4)
            if int(output) == 4:
                if self.beamer_4 != "":
                    self.beamer_4.off(bytes.fromhex(self.config.get("beamer4", "input_off")))
                    self.powerstrip_labor.switch_off(1)
        else:
            self.hdmi_controller.set_input = inp
            self.hdmi_controller.set_output = output
            self.hdmi_controller.toggle_connection()

    def hdmi_status(self, output):
        feedback = self.hdmi_switch.output_connections(output)
        return feedback

    # change beamer state of given beamer
    def control_beamer(self, number_beamer):
        if number_beamer == "1":
            if self.beamer_1 != "":
                if self.powerstrip_studio.status(1) != 1:
                    self.powerstrip_studio.switch_on(1)
                    time.sleep(2)
                    self.beamer_1.on(bytes.fromhex(self.config.get("beamer1", "input_on")))     
                else:
                    self.beamer_1.off(bytes.fromhex(self.config.get("beamer1", "input_off")))
                    self.powerstrip_studio.switch_off(1)
        if number_beamer == "2":
            if self.beamer_2 != "":
                if self.powerstrip_studio.status(4) != 1:
                    self.powerstrip_studio.switch_on(4)
                    time.sleep(2)
                    self.beamer_2.on(bytes.fromhex(self.config.get("beamer2", "input_on")))     
                else:
                    self.beamer_2.off(bytes.fromhex(self.config.get("beamer2", "input_off")))
                    self.powerstrip_studio.switch_off(4)
        if number_beamer == "3":
            if self.beamer_3 != "":
                if self.powerstrip_labor.status(4) != 1:
                    self.powerstrip_labor.switch_on(4)
                    time.sleep(2)
                    self.beamer_3.on(bytes.fromhex(self.config.get("beamer3", "input_on")))     
                else:
                    self.beamer_3.off(bytes.fromhex(self.config.get("beamer3", "input_off")))
                    self.powerstrip_labor.switch_off(4)
        if number_beamer == "4":
            if self.beamer_4 != "":
                print(self.powerstrip_labor.status(1))
                if self.powerstrip_labor.status(1) != 1:
                    self.powerstrip_labor.switch_on(1)
                    time.sleep(2)
                    self.beamer_4.on(bytes.fromhex(self.config.get("beamer4", "input_on")))     
                else:
                    self.beamer_4.off(bytes.fromhex(self.config.get("beamer4", "input_off")))
                    self.powerstrip_labor.switch_off(1)        

    # switch on or off light in dependence of the status return
    def control_light(self):
        if self.powerstrip_studio.status(3) == 1:
            self.powerstrip_studio.switch_off(3)
            return "off"
        else:
            self.powerstrip_studio.switch_on(3)
            return "on"

    # switch on or off the free available sockets in dependence of the status return
    def control_powerstrip(self, room, socket):
        if room == "1":
            if self.powerstrip_studio.status(int(socket)) == 1:
                self.powerstrip_studio.switch_off(int(socket))
                return "off"
            else:
                self.powerstrip_studio.switch_on(int(socket))
                return "on"
        else:
            print("status labor", self.powerstrip_labor.status(int(socket)))
            if self.powerstrip_labor.status(int(socket)) == 1:
                self.powerstrip_labor.switch_off(int(socket))
                return "off"
            else:
                self.powerstrip_labor.switch_on(int(socket))
                return "on"

    def status_powerstrip_labor(self):
        status_2 = self.powerstrip_labor.status(2)
        status_3 = self.powerstrip_labor.status(3)
        status_beamer4 = self.powerstrip_labor.status(1)
        status_beamer3 = self.powerstrip_labor.status(4)
        status = {'2': status_2, '3': status_3, 'beamer_3': status_beamer3, 'beamer_4': status_beamer4}
        return status

    def status_powerstrip_studio(self):
        status_beamer1 = self.powerstrip_labor.status(1)
        status_beamer2 = self.powerstrip_labor.status(4)
        status = {'beamer_1': status_beamer1, 'beamer_2': status_beamer2}
        return status

    # switch to given usb output
    def control_usb_switch(self, output):
        print("controller usb switch")
        self.usb_switch.change_to_number(int(output))

