#!/usr/bin/env python3

import sys
import random
import time
import json
import signal
import os
import os.path

import tornado.ioloop
import tornado.websocket
import tornado.httpserver

from arduino_gen import ArduinoGen
from decorators import attr_check, type_check


clients = set()
client_id = 0

port = 9000
current_arduino_code_folder = "/Robot/CurrentArduinoCode"
conf_folder = "./conf"
lock_folder = "/var/lock"
pin = random.randint(0, 99999)

current_arduino_code_folder_abs_path = os.path.abspath(current_arduino_code_folder)
if not os.path.isdir(current_arduino_code_folder_abs_path):
    os.mkdir(current_arduino_code_folder_abs_path)

conf_folder_abs_path = os.path.abspath(conf_folder)
if not os.path.isdir(conf_folder_abs_path):
    os.mkdir(conf_folder_abs_path)

lock_folder_abs_path = os.path.abspath(lock_folder)
if not os.path.isdir(lock_folder_abs_path):
    os.mkdir(lock_folder_abs_path)


arduinos = [{"name": d} for d in os.listdir(current_arduino_code_folder)
            if os.path.isdir(current_arduino_code_folder + "/" + d) and not d == ".git"]

for arduino in arduinos:
    arduino["locked"] = os.path.exists(lock_folder_abs_path + "/" + arduino["name"] + ".lck")

@type_check
def log(wsId: int, message: str): -> None
    print(("{}\tClient {:2d}\t{}".format(
        time.strftime("%H:%M:%S", time.localtime()), wsId, message
    )))


@attr_check
class Server(tornado.websocket.WebSocketHandler):

    id_ = int
    verified = bool

    @type_check
    def check_origin(self, origin): -> bool
        return True

    @type_check
    def open(self): -> None
        global clients, client_id

        self.id_ = client_id
        client_id += 1
        clients.add(self)

        self.verified = False

        log(self.id, "connected with ip: " + self.request.remote_ip)

    @type_check
    def on_message(self, message: str): -> None
        if not self.verified:
            try:
                clientPin = int(message)
            except ValueError:
                self.write_message("Invalid Pin")
                log(self.id, "entered an invalid pin: " + message)
                return

            if clientPin == pin:
                self.verified = True
                self.write_message("Verified")
                log(self.id, "entered correct pin")
            else:
                self.write_message("WrongPin")
                log(self.id, "entered wrong pin")

            self.write_message("DeviceList" + json.dumps(arduinos))

        else:
            cmd = "Lock"
            if message[:len(cmd)] == cmd:
                if hasattr(self, 'device'):
                    self.write_message("ClientHasLock")
                    log(self.id, "tried to lock, but already has a device lock")
                else:
                    dev_name = message[len(cmd):]

                    dev = list([x for x in arduinos if x["name"] == dev_name])
                    if len(dev):
                        dev = dev[0]
                    else:
                        self.write_message("DeviceNotRegistered")
                        log(self.id, dev_name + " device not registered")
                        return

                    if dev["locked"]:
                        self.write_message("DeviceInUse")
                        log(self.id, dev_name + " device is in use")
                    else:
                        dev["locked"] = True
                        self.device = dev
                        lock_filename = lock_folder_abs_path + "/" + self.device["name"] + ".lck"
                        with open(lock_filename, "w") as f:
                            f.write("Locked by ArduinoGenServer")
                        os.chmod(lock_filename, 0o777)
                        for client in clients:
                            client.write_message("DeviceList" + json.dumps(arduinos))
                        log(self.id, "updated devices")

                        self.write_message("LockedDevice" + dev_name)
                        log(self.id, "locked " + dev_name)
                return

            cmd = "Unlock"
            if message[:len(cmd)] == cmd:
                if not hasattr(self, 'device'):
                    self.write_message("ClientNoLock")
                    log(self.id, "tried to unlock, but doesn't have a device lock")
                else:
                    lock_filename = lock_folder_abs_path + "/" + self.device["name"] + ".lck"
                    os.remove(lock_filename)
                    self.device["locked"] = False
                    self.write_message("UnlockedDevice" + self.device["name"])
                    log(self.id, "unlocked " + self.device["name"])
                    del self.device

                    for client in clients:
                        client.write_message("DeviceList" + json.dumps(arduinos))
                    log(self.id, "updated devices")
                return

            cmd = "GetComponents"
            if message[:len(cmd)] == cmd:
                if not hasattr(self, 'device'):
                    self.write_message("ClientNoLock")
                    log(self.id, "tried to get components, but doesn't have a device lock")
                else:
                    device_json_file = current_arduino_code_folder + "/" + self.device["name"] + "/" + \
                        self.device["name"] + ".json"
                    if not os.path.exists(device_json_file):
                        self.write_message("[]")
                        log(self.id, "no file, sending empy list")
                    else:
                        with open(device_json_file, 'r') as json_file:
                            json_data = json_file.read().replace('\n', '')
                            self.write_message("ComponentList" + json_data)
                            log(self.id, "requested " + self.device["name"] + "'s components")
                return

            cmd = "PostComponents"
            if message[:len(cmd)] == cmd:
                if not hasattr(self, 'device'):
                    self.write_message("ClientNoLock")
                    log(self.id, "tried to post components, but doesn't have a device lock")
                else:
                    device_json_file = conf_folder_abs_path + "/" + self.device["name"] + ".json"
                    with open(device_json_file, 'w') as json_file:
                        json_file.write(message[len(cmd):])
                        self.write_message("PostedComponents")
                        log(self.id, "posted " + self.device["name"] + "'s components")
                return

            cmd = "GenCode"
            if message[:len(cmd)] == cmd:
                if not hasattr(self, 'device'):
                    self.write_message("ClientNoLock")
                    log(self.id, "tried to generate arduino code, but doesn't have a device lock")
                else:
                    device_json_file = conf_folder_abs_path + "/" + self.device["name"] + ".json"
                    with open(device_json_file, 'w') as json_file:
                        json_file.write(message[len(cmd):])
                        self.write_message("PostedComponents")
                        log(self.id, "posted " + self.device["name"] + "'s components")

                    log(self.id, "generating arduino code for " + self.device["name"])

                    ag = ArduinoGen(arduino=self.device["name"])
                    ag.setParentFolder(os.path.dirname(os.path.realpath(__file__)))
                    ag.setupFolder()
                    ag.readConfig(device_json_file)
                    ag.generateOutput()
                    log(self.id, "generated arduino code for " + self.device["name"])
                    self.write_message("GeneratedArduinoCode")
                return

            cmd = "WriteComponents"
            if message[:len(cmd)] == cmd:
                if not hasattr(self, 'device'):
                    self.write_message("ClientNoLock")
                    log(self.id, "tried to write components, but doesn't have a device lock")
                else:
                    device_json_file = conf_folder_abs_path + "/" + self.device["name"] + ".json"
                    with open(deviceJsonFile, 'w') as json_file:
                        json_file.write(message[len(cmd):])
                        self.write_message("PostedComponents")
                        log(self.id, "posted " + self.device["name"] + "'s components")

                    log(self.id, "writing components to " + self.device["name"])

                    ag = ArduinoGen(arduino=self.device["name"])
                    ag.setParentFolder(os.path.dirname(os.path.realpath(__file__)))
                    ag.setupFolder()
                    ag.readConfig(device_json_file)
                    ag.generateOutput()
                    ag.upload()
                    log(self.id, "written components to " + self.device["name"])
                    self.write_message("WrittenComponents")
                return

    @type_check
    def on_close(self): -> None
        if hasattr(self, 'device'):
            dev = self.device
            dev["locked"] = False
            lockFileName = lockFolderAbsPath + "/" + dev["name"] + ".lck"
            os.remove(lockFileName)
            log(self.id, "unlocked " + dev["name"])

            clients.remove(self)

            for client in clients:
                client.write_message("DeviceList" + json.dumps(arduinos))
            log(self.id, "updated devices")
        else:
            clients.remove(self)

        log(self.id, "disconnected")


@attr_check
class SetupTLS(tornado.web.RequestHandler):
    @type_check
    def get(self): -> None
        self.write("Please accept the TLS certificate to use websockets from this device.")

@type_check
def make_app(): -> tornado.httpserver.HTTPServer
    return tornado.httpserver.HTTPServer(tornado.web.Application([
        (r"/", Server),
        (r"/setuptls", SetupTLS)
    ]), ssl_options={
        "certfile": "/etc/ssl/certs/tornado.crt",
        "keyfile": "/etc/ssl/certs/tornado.key"
    })

@type_check
def sigInt_handler(signum, frame): -> None
    print("Closing Server")

    while clients:
        client = next(iter(clients))
        client.close(reason="Server Closing")
        client.on_close()

    tornado.ioloop.IOLoop.current().stop()
    print("Server is closed")
    sys.exit(0)


if __name__ == "__main__":
    app = make_app()
    app.listen(port)
    signal.signal(signal.SIGINT, sigInt_handler)
    print(("Pin: {:05d}".format(pin)))
    tornado.ioloop.IOLoop.current().start()
