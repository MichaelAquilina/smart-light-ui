#! /usr/bin/python3
import os

from phue import Bridge

import gi
gi.require_version('Gtk', '3.0')  # noqa

from gi.repository import Gtk


class SmartLightWindow(Gtk.Window):

    def __init__(self, bridge_ip):
        Gtk.Window.__init__(
            self, title="Smart Bulb Controller",
        )
        self.resize(600, 100)

        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.set_title(self.get_title())
        self.set_titlebar(self.header)

        self.box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=6,
            margin=10,
            expand=True
        )
        self.add(self.box)

        self.setup_phue(bridge_ip)

    def setup_phue(self, bridge_ip):
        self.bridge = Bridge(bridge_ip)
        self.bridge.connect()

        for light in self.bridge.lights:
            light_scale = Gtk.HScale(
                digits=0,
                valign=Gtk.Align.START,
                adjustment=Gtk.Adjustment(
                    lower=0,
                    upper=255,
                    value=light.brightness,
                    step_increment=1,
                    page_increment=1,
                )
            )
            light_scale.connect('value-changed', self.toggle_light_brightness, light)

            light_button = Gtk.Switch(active=light.on)
            light_button.connect('notify::active', self.toggle_light_power, light)

            light_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            light_box.pack_start(light_button, False, False, 0)
            light_box.pack_start(light_scale, True, True, 0)

            self.box.add(Gtk.Label(label=light.name))
            self.box.add(light_box)

    def toggle_light_brightness(self, widget, light):
        light.brightness = int(widget.get_value())

    def toggle_light_power(self, switch, gparam, light):
        light.on = switch.get_active()


if __name__ == '__main__':
    win = SmartLightWindow(os.environ["SMART_BRIDGE_IP"])
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()