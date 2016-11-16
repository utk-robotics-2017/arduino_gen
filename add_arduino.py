import argparse
import pyudev
import usb.core


class LocalDevice:
    def __init__(self):
        self.device_name = device_name
        self.vendor_id = vendor_id
        self.product_id = product_id


class AddArduino:
    def __init__(self):
        self.context = pyudev.Context()
        self.usb = usb.core
        self.unnamed = []
        self.named = []

    def fill_lists(self):
        for device in context.list_devices():
            

    def display_lists(self):
        pass

    def name(self):
        pass

    def unname(self):
        pass

if __name__ == "__main__":
    aa = AddArduino()
