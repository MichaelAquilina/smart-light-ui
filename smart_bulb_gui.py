#! /usr/bin/python3
import os

import phue_bulb

import gi
gi.require_version('Gtk', '3.0')  # noqa

from gi.repository import Gtk  # noqa


class SmartLightWindow(Gtk.Window):

    def __init__(self, bridge_ip):
        Gtk.Window.__init__(
            self,
            title="Smart Bulb Controller",
            icon_name="dialog-information",
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

        self.lights = []
        self.lights.extend(phue_bulb.get_phue_bulbs(bridge_ip))
        self.setup_ui()

        self.global_switch = Gtk.Switch(active=True)
        self.global_switch.connect('notify', self.toggle_all_lights)

        self.header.pack_end(self.global_switch)

    def setup_ui(self):
        self.light_buttons = {}
        self.light_scales = {}

        for light in self.lights:
            light_scale = Gtk.HScale(
                digits=2,
                valign=Gtk.Align.START,
                adjustment=Gtk.Adjustment(
                    lower=0,
                    upper=1.0,
                    value=light.get_brightness(),
                    step_increment=0.05,
                    page_increment=0.05,
                )
            )
            light_scale.connect('value-changed', self.toggle_light_brightness, light)

            light_button = Gtk.Switch(active=light.get_power())
            light_button.connect('notify::active', self.toggle_light_power, light)

            light_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            light_box.pack_start(light_button, False, False, 0)
            light_box.pack_start(light_scale, True, True, 0)

            self.box.add(Gtk.Label(label=light.get_name()))
            self.box.add(light_box)

            self.light_scales[light] = light_scale
            self.light_buttons[light] = light_button

    def toggle_light_brightness(self, widget, light):
        light.set_brightness(widget.get_value())

    def toggle_light_power(self, switch, gparam, light):
        light.set_power(switch.get_active())

    def toggle_all_lights(self, switch, gparam):
        if not switch.get_active():
            for light in self.lights:
                light.set_power(False)
        else:
            for light, light_button in self.light_buttons.items():
                light.set_power(light_button.get_active())


if __name__ == '__main__':
    win = SmartLightWindow(os.environ["SMART_BRIDGE_IP"])
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
