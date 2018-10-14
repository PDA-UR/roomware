#!/usr/bin/python3
# -*- coding: utf-8 -*-


class PropertiesTemplate():
    
    def __init__(self):
        super().__init__()
        self.template = {'beamer_headline_1': 'off', 'beamer_onoff_1': 'beamer_off', 'beamer_headline_2': 'off', 'beamer_onoff_2': 'beamer_off', 'beamer_headline_3': 'off', 'beamer_onoff_3': 'beamer_off', 'beamer_headline_4': 'off', 'beamer_onoff_4': 'beamer_off', 'beamer_11': 'output_off', 'beamer_12': 'output_off', 'beamer_13': 'output_off', 'beamer_14': 'output_off', 'beamer_21': 'output_off', 'beamer_22': 'output_off', 'beamer_23': 'output_off', 'beamer_24': 'output_off','beamer_31': 'output_off', 'beamer_32': 'output_off', 'beamer_33': 'output_off', 'beamer_34': 'output_off', 'beamer_41': 'output_off', 'beamer_42': 'output_off', 'beamer_43': 'output_off', 'beamer_44': 'output_off', 'powerstrip_1': 'off', 'powerstrip_2': 'off', 'socket_12': 'output_off', 'socket_22': 'output_off', 'socket_23': 'output_off', 'light_1': 'off', 'lamp_1': 'light_off', 'stream': 'output_off', 'usb': 'off', 'usb_output_2': 'output_off', 'usb_output_3': 'output_off', 'usb_output_4': 'output_off'}

    def get_template(self):
        return self.template

    def change_template(self, key, value):
        self.template[key] = value
    
