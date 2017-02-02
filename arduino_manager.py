import pyudev
import usb.core
import os
import shutil
from subprocess import call

CURRENT_ARDUINO_CODE_DIR = "/Robot/CurrentArduinoCode"
ARDUINO_UDEV_RULES = "/etc/udev/rules.d/100-arduino-usb-serial.rules"


class LocalDevice:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "No Name")
        self.type = kwargs.get("type", "No Type")
        self.vendor = kwargs.get("vendor", "No Vendor")
        self.product = kwargs.get("product", "No Product")
        self.serial_number = kwargs.get("serial_number", "No Serial Number")

    def toUdevRule(self):
        return 'SUBSYSTEM=="tty", ATTRS{{idVendor}}=="{:04x}", ATTRS{{idProduct}}=="{:04x}",'
        + ' ATTRS{{serial}}=="{}", SYMLINK+="{}"\n'.format(
            self.vendor, self.product, self.serial_number, self.name)

    def __str__(self):
        return "\tName: {0:}\n\tType: {1:}\n\tVendor: 0x{2:04x}\n\tProduct: 0x{3:04x}\n"
        + "\tSerial Number: {4:}".format(
            self.name, self.type, self.vendor, self.product, self.serial_number)

    def __repr__(self):
        self.__str__()


class UdevRule:
    def __init__(self, text):
        text_split = text.split('"')
        self.subsystem = text_split[1]
        self.vendor = text_split[3]
        self.product = text_split[5]
        self.serial_number = text_split[7]
        self.symlink = text_split[9]


class ArduinoManager:
    def __init__(self):
        self.context = pyudev.Context()
        self.usb = usb.core
        self.unnamed = {}
        self.named = {}
        self.udev_rules = {}
        self.current_arduinos = os.listdir(CURRENT_ARDUINO_CODE_DIR)

    def fill_lists(self):
        self.count = 0
        for device in self.usb.find(find_all=1):
            if(device is None or device.product is None):
                continue
            if "arduino" in device.product.lower():
                type = "Uno" if "uno" in device.product.lower() else "Mega"
                self.unnamed[self.count] = LocalDevice(
                    type=type,
                    vendor=device.idVendor,
                    product=device.idProduct,
                    serial_number=device.serial_number
                )
                self.count += 1

        self.udev_rules = {}
        mode = 'r' if os.path.exists(ARDUINO_UDEV_RULES) else 'w+'
        for line in open(ARDUINO_UDEV_RULES, mode):
            udev_rule = UdevRule(line)
            self.udev_rules[udev_rule.serial_number] = udev_rule

        del_list = []
        for name, device in self.unnamed.items():
            if device.serial_number in self.udev_rules:
                device.name = self.udev_rules[device.serial_number].symlink
                self.named[device.name] = device
                del_list.append(name)
        for item in del_list:
            del self.unnamed[item]

    def display_lists(self):
        print("Named:")
        for name, device in self.named.items():
            print(device)
        print("Unnamed:")
        for name, device in self.unnamed.items():
            print("Device [{}]".format(name))
            print(device)

    def name(self, index, device_name):
        if index in self.unnamed:
            device = self.unnamed[index]
            del self.unnamed[index]
            device.name = device_name
            self.named[device_name] = device
            if not os.path.exists(CURRENT_ARDUINO_CODE_DIR + "/" + device.name):
                os.mkdir(CURRENT_ARDUINO_CODE_DIR + "/" + device.name)
            if not os.path.exists(CURRENT_ARDUINO_CODE_DIR + "/" + device.name + "/platformio.ini"):
                with open(
                    CURRENT_ARDUINO_CODE_DIR + "/" + device.name + "/platformio.ini", "w+"
                ) as f:
                    f.write("[platformio]\n")
                    f.write("lib_dir = /Robot/ArduinoLibraries\n")
                    f.write("env_default = {}\n\n".format(device.name))
                    f.write("[env:{}]\n".format(device.name))
                    f.write("platform = atmelavr\n")
                    f.write("framework = arduino\n")
                    f.write("board = {}\n".format(
                        "megaatmega2560" if device.type == "Mega"
                        else "uno"
                    ))
                    f.write("upload_port = /dev/{}\n".format(device.name))
        else:
            print("No unnamed arduino {}".format(index))

    def edit_name(self, old_name, new_name):
        if old_name in self.named:
            self.named[new_name] = self.named[old_name]
            del self.named[old_name]
            self.named[new_name].name = new_name
        else:
            print("No arduino named {} exists".format(old_name))

    def unname(self, old_name):
        if old_name in self.named:
            shutil.rmtree(CURRENT_ARDUINO_CODE_DIR + "/" + old_name)
            self.unnamed[self.count] = self.named[old_name]
            self.unnamed[self.count].name = "No Name"
            del self.named[old_name]
            self.count += 1
        else:
            print("No arduino named {} exists".format(old_name))

    def save_udev(self):
        with open(ARDUINO_UDEV_RULES, 'w') as f:
            for name, device in self.named.items():
                f.write(device.toUdevRule())


def display_commands():
    print("Commands:")
    print("\tname <device number> <device name>")
    print("\tedit-name <old name> <new name>")
    print("\tunname <device name>")
    print("\tquit")
    print("\texit")


if __name__ == "__main__":
    if os.getuid() != 0:
        print("ArduinoManager must be run with sudo")
        exit()

    manager = ArduinoManager()
    manager.fill_lists()
    manager.display_lists()
    while True:
        display_commands()
        line = input('>')
        line_split = line.split(' ')
        if line_split[0] == 'name':
            if len(line_split) != 3:
                print("Incorrect Number of Arguments")
                continue

            try:
                device_index = int(line_split[1])
            except:
                print("Incorrect Argument")
                continue
            manager.name(int(line_split[1]), line_split[2])
        elif line_split[0] == 'edit-name':
            if len(line_split) != 3:
                print("Incorrect Number of Arguments")
                continue

            manager.edit_name(line_split[1], line_split[2])
        elif line_split[0] == 'unname':
            if len(line_split) != 2:
                print("Incorrect Argument")
                continue
            manager.unname(line_split[1])
        elif line_split[0] in ['quit', 'exit']:
            manager.save_udev()
            call(['udevadm', 'trigger'])
            break
        else:
            print("Unknown command")
