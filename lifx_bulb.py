# -*- coding: utf-8 -*-

import pylifx


def get_lifx_bulbs(mac_address):
    controller = pylifx.LifxController(mac_address)
    return [LifxBulb(controller)]


class LifxBulb(object):

    def __init__(self, light):
        self.light = light

    def get_power(self):
        return True

    def set_power(self, value):
        if value:
            self.light.on()
        else:
            self.light.off()

    def get_brightness(self):
        return 1.0

    def set_brightness(self, value):
        self.light.set_rgb(value, value, value, fadeTime=0.06)

    def get_name(self):
        return 'Lifx Controller'
        # return self.light.label
