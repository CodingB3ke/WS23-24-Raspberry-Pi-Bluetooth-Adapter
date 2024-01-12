#!/usr/bin/python3
# SPDX-License-Identifier: LGPL-2.1-or-later

# accept command-line options and arguments
import argparse
# D-Bus is message bus system for inter-process communication
import dbus
import dbus.service
# GLib main loop as default main loop
import dbus.mainloop.glib
from gi.repository import GLib

# name for BlueZ (Linux Bluetooth stack)
BUS_NAME = 'org.bluez'
# adapter interface name
AGENT_INTERFACE = 'org.bluez.Agent1'
# agent path
AGENT_PATH = "/speaker/agent"
# object identifier for bluetooth on dbus
OBJECT_PATH = '/org/bluez/hci0'
# interface to interact with BlueZ properties
PROP_INTERFACE = 'org.freedesktop.DBus.Properties'

# transfer standard for transfer of audio signals via Bluetooth
A2DP = '0000110d-0000-1000-8000-00805f9b34fb'
# standard for audio and video remote control
AVRCP = '0000110e-0000-1000-8000-00805f9b34fb'
# standard for hands free profile (f.g. phones) -> could be added to uuid
HFP = '0000111e-0000-1000-8000-00805f9b34fb'


# error handling for exceptions (such as unknown service)
class Rejected(dbus.DBusException):
    _dbus_error_name = "org.bluez.Error.Rejected"


# Agent is a class that can be interacted with via the dbus -> inherited from dbus.service.object
class Agent(dbus.service.Object):
    # initialize agent
    def __init__(self, bus, path):
        self.exit_on_release = True
        self.remote_device = None
        # because of inheritance, the dbus service object needs to be initialized
        dbus.service.Object.__init__(self, bus, path)

    def set_exit_on_release(self, exit_on_release):
        self.exit_on_release = exit_on_release

    # release function to be accessed by Dbus via Agent interface
    @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
    def Release(self):
        print("Release")
        # if program should be closed after release, mainloop is quit
        if self.exit_on_release:
            GPIO.cleanup()
            mainloop.quit()

    # release function to be accessed by Dbus via Agent interface
    # in signature: 'o' = Object path
    # in signature: 's' = string
    @dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
    def AuthorizeService(self, device, uuid):
        # error handling of connection
        if self.remote_device and self.remote_device != device:
            print("%s try to connect while %s already connected" % (device, self.remote_device))
            raise Rejected("Connection rejected by user")

        # Always authorize A2DP, AVRCP connection
        if uuid in [A2DP, AVRCP]:
            print("AuthorizeService (%s, %s)" % (device, uuid))
            return
        else:
            # reject unknown services
            print("Service rejected (%s, %s)" % (device, uuid))
        # dbus exception documented
        raise Rejected("Connection rejected by user")


    # cancel function to be accessed by Dbus via interface
    # occurs for example if phone is unable to pair
    @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
    def Cancel(self):
        print("Cancel")


def start_speaker_agent():
    # Set bluetooth adapter as always discoverable
    adapter = dbus.Interface(bus.get_object(BUS_NAME, OBJECT_PATH),            # construction of dbus interface object for shortcut
                             PROP_INTERFACE)
    adapter.Set("org.bluez.Adapter1", "DiscoverableTimeout", dbus.UInt32(0))   # remove discoverable time out
    adapter.Set("org.bluez.Adapter1", "Discoverable", True)                    # always discoverable

    print("Raspberry Pi Bluetooth Adapter discoverable")

    # creating pairing agent
    obj = bus.get_object(BUS_NAME, "/org/bluez")
    manager = dbus.Interface(obj, "org.bluez.AgentManager1")
    manager.RegisterAgent(AGENT_PATH, "NoInputNoOutput")        # no user input nor output required for pairing

    print("Agent registered")

    manager.RequestDefaultAgent(AGENT_PATH)


# event handeling if org.bluez appears on dbus
def nameownerchanged_handler(*args, **kwargs):
    if not args[1]:
        print('org.bluez appeared')
        # agent is needed to manage pairing
        start_speaker_agent()


if __name__ == '__main__':
  # this is for calling the script via service
  options = argparse.ArgumentParser(description="BlueZ Speaker Agent")
  args = options.parse_args()

  # sets new dbus mainloop to work with glib mainloop -> glib mainloop will be the running main loop
  # this ensures handling of dbus events while glib mainloop is running
  dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
  # connect to System bus via bus object
  bus = dbus.SystemBus()
  # create instance of agent
  agent = Agent(bus, AGENT_PATH)
  agent.set_exit_on_release(False)
  # event handler when matching signal is received on system bus
  bus.add_signal_receiver(nameownerchanged_handler,               # handler function
                          signal_name='NameOwnerChanged',         # signal to use when new names appear on dbus
                          dbus_interface='org.freedesktop.DBus',  # standard interface for dbus
                          path='/org/freedesktop/DBus',           # path to standard interface
                          interface_keyword='dbus_interface',     # keyword argument for handler function
                          arg0=BUS_NAME                           # additional argument for handler **kwargs
                          )
  # check if Bluez is already running
  # create another instance of org.freedesktop.DBus
  dbus_service = bus.get_object('org.freedesktop.DBus',
                                '/org/freedesktop/DBus')
  dbus_dbus = dbus.Interface(dbus_service, 'org.freedesktop.DBus')
  # check if Bluez is already running
  if dbus_dbus.NameHasOwner(BUS_NAME):
      print('org.bluez already started')
      # start speaker agent in case of error
      start_speaker_agent()

  mainloop = GLib.MainLoop()
  mainloop.run()
