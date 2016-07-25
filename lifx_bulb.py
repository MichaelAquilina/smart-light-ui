# -*- coding: utf-8 -*-

import lifxlan


def get_lifx_bulbs():
    return [LifxBulb(l) for l in lifxlan.LifxLAN(1).get_lights()]


class LifxBulb(object):

    def __init__(self, light):
        self.light = light

    def get_power(self):
        return bool(self.light.get_power())

    def set_power(self, value):
        self.light.set_power(value)

    def get_brightness(self):
        return self.light.get_color()[0] / 65535.0

    def set_brightness(self, value):
        value *= 65535
        value = int(value)
        self.light.set_color((value, value, value, value), duration=0.06)

    def get_name(self):
        return 'Lifx ()'

    def __repr__(self):
        return '<LifxBulb: {}>'.format(self.light._name)
