# -*- coding: utf-8 -*-
from phue import Bridge


def get_phue_bulbs(ip_address):
    bridge = Bridge(ip_address)
    bridge.connect()

    return [PhueBulb(light) for light in bridge.lights]


class PhueBulb(object):

    def __init__(self, light):
        self.light = light

    def set_power(self, on):
        self.light.on = on

    def get_power(self):
        return self.light.on

    def get_brightness(self):
        return self.light.brightness / 255.0

    def set_brightness(self, value):
        self.light.brightness = int(value * 255)

    def get_name(self):
        return self.light.name
