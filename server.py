#!/usr/bin/env python3

import sys
import random
import time
import json
import signal
import os

from tornado.websocket import WebSocketHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

from arduino_gen import ArduinoGen
from appendages.util.logger import Logger
logger = Logger()


class Server(WebSocketHandler):
    clients = set()
    client_id = 0

    current_arduino_code_filepath = "/Robot/CurrentArduinoCode"
    config_folder_filepath = os.path.abspath("./config")
    lock_folder_filepath = "/var/lock"

    arduinos = [{"name": d, "locked": os.path.exists("{0:s}/{1:s}.lck".format(lock_folder_filepath, d))}
                for d in os.listdir(current_arduino_code_filepath)
                if os.path.isdir("{0:s}/{1:s}".format(current_arduino_code_filepath, d)) and not d == ".git"]

    pin = random.randint(0, 99999)

    def __init__(self, *args, **kwargs):
        self.setup_folders()

        self.commands = {"Lock": self.Lock,
                         "Unlock": self.unlock,
                         "GetComponents": self.get_components,
                         "PostCompoents": self.post_components,
                         "GenCode": self.generate_code,
                         "WriteComponents": self.write_components}

        WebSocketHandler.__init__(self, *args, **kwargs)

    def setup_folders(self):
        if not os.path.isdir(self.current_arduino_code_filepath):
            os.mkdir(self.current_arduino_code_filepath)

        if not os.path.isdir(self.config_folder_filepath):
            os.mkdir(self.config_folder_filepath)

        if not os.path.isdir(self.lock_folder_filepath):
            os.mkdir(self.lock_folder_filepath)

    def log(self, message):
        logger.info("{}\tClient {:2d}\t{}".format(time.strftime("%H:%M:%S", time.localtime()), self.id, message))

    def check_origin(self, origin):
        return True

    def open(self):
        self.id = self.client_id
        self.client_id += 1
        self.clients.add(self)

        self.verified = False

        self.log("connected with ip: {0:s}".format(self.request.remote_ip))

    def on_message(self, message):
        if not self.verified:
            try:
                client_pin = int(message)
            except ValueError:
                self.write_message("Invalid Pin")
                self.log("entered an invalid pin: " + message)
                return

            if client_pin == self.pin:
                self.verified = True
                self.write_message("Verified")
                self.log("entered correct pin")
            else:
                self.write_message("WrongPin")
                self.log("entered wrong pin")

            self.write_message("DeviceList" + json.dumps(self.arduinos))

        else:
            for command_key in self.commands:
                if message[:len(command_key)] == command_key:
                    self.commands[command_key](message[len(command_key):])
                    return
            logger.error("{0:s}\tClient {1:2d}\tUnknown command: {2:s}"
                         .format(time.strftime("%H:%M:%S", time.localtime()), self.id, message))

    def lock(self, message):
        if hasattr(self, 'device'):
            self.write_message("ClientHasLock")
            self.log(id, "tried to lock, but already has a device lock")
        else:
            device_name = message
            device = None
            for arduino in self.arduinos:
                if arduino['name'] == device_name:
                    device = arduino
                    break
            if device is None:
                self.write_message("DeviceNotRegistered")
                self.log("{0:s} device not registered".format(device_name))
                return

            if device['locked']:
                self.write_message("DeviceInUse")
                self.log("{0:s} device is in use".format(device_name))
                return

            device["locked"] = True
            self.device = device
            lock = "{0:s}/{1:s}.lck".format(self.lock_folder_filepath, self.device['name'])
            with open(lock, "w") as f:
                f.write("Locked by ArduinoGenServer")
            os.chmod(lock, 0o777)
            for client in self.clients:
                client.write_message("DeviceList" + json.dumps(self.arduinos))
            self.log("updated devices")

            self.write_message("LockedDevice" + device_name)
            self.log("locked " + device_name)

    def unlock(self, message):
        if not hasattr(self, 'device'):
            self.write_message("ClientNoLock")
            self.log("Tried to unlock device but the device isn't locked")
            return

        lock = "{0:s}/{1:s}.lck".format(self.lock_folder_filepath, self.device['name'])
        os.remove(lock)
        self.device['locked'] = False
        self.write_message("UnlockedDevice" + self.device["name"])
        self.log("unlocked " + self.device["name"])
        del self.device
        for client in self.clients:
            client.write_message("DeviceList" + json.dumps(self.arduinos))
        self.log("updated devices")

    def get_components(self, message):
        if not hasattr(self, 'device'):
            self.write_message("ClientNoLock")
            self.log("tried to get components, but doesn't have a device lock")
        else:
            device_file = "{0:s}/{1:s}/{1:s}.json".format(self.current_arduino_code_filepath,
                                                          self.device["name"])
            if not os.path.exists(device_file):
                self.write_message("[]")
                self.log("no file, sending empy list")
            else:
                with open(device_file, 'r') as json_file:
                    json_data = json_file.read().replace('\n', '')
                    self.write_message("ComponentList" + json_data)
                    self.log("requested {0:s}'s components".format(self.device["name"]))

    def post_components(self, message):
        if not hasattr(self, 'device'):
            self.write_message("ClientNoLock")
            self.log("tried to post components, but doesn't have a device lock")
        else:
            device_file = "{0:s}/{1:s}.json".format(self.config_folder_filepath, self.device["name"])
            with open(device_file, 'w') as json_file:
                json_file.write(message)
            self.write_message("PostedComponents")
            self.log("posted {0:s}'s components".format(self.device['name']))

    def generate_code(self, message):
        if not hasattr(self, 'device'):
            self.write_message("ClientNoLock")
            self.log("tried to generate arduino code, but doesn't have a device lock")
        else:
            device_file = "{0:s}/{1:s}.json".format(self.config_folder_filepathself.device["name"])
            with open(device_file, 'w') as json_file:
                json_file.write(message)
            self.write_message("PostedComponents")
            self.log("posted {0:s}'s components".format(self.device["name"]))

            self.log("generating arduino code for {0:s}".format(self.device["name"]))

            arduino_gen = ArduinoGen(arduino=self.device["name"])
            arduino_gen.set_parent_folder(os.path.dirname(os.path.realpath(__file__)))
            arduino_gen.setup_folder()
            arduino_gen.read_config(device_file)
            arduino_gen.generate_output()
            self.log("generated arduino code for {0:s}".format(self.device["name"]))
            self.write_message("GeneratedArduinoCode")

    def write_components(self, message):
        if not hasattr(self, 'device'):
            self.write_message("ClientNoLock")
            self.log("tried to write components, but doesn't have a device lock")
        else:
            device_file = "{0:s}/{1:s}.json".format(self.config_folder_filepath, self.device["name"])
            with open(device_file, 'w') as jsonFile:
                jsonFile.write(message)
            self.write_message("PostedComponents")
            self.log("posted {0:s}'s components".format(self.device["name"]))

            self.log("writing components to {0:s}".format(self.device["name"]))

            arduino_gen = ArduinoGen(arduino=self.device["name"])
            arduino_gen.set_parent_folder(os.path.dirname(os.path.realpath(__file__)))
            arduino_gen.setup_folder()
            arduino_gen.read_config(device_file)
            arduino_gen.generate_output()
            arduino_gen.upload()
            self.log("written components to {0:s}".format(self.device["name"]))
            self.write_message("WrittenComponents")

    @classmethod
    def stop(cls):
        for client in cls.clients:
            client.close(Reason="Server closing")
            client.on_close()

    def on_close(self):
        if hasattr(self, 'device'):
            self.device["locked"] = False
            lock = "{0:s}/{1:s}.lck".format(self.lock_folder_filepath,  self.device["name"])
            os.remove(lock)
            self.log("unlocked {0:s}".format(self.device["name"]))

            self.clients.remove(self)

            for client in self.clients:
                client.write_message("DeviceList" + json.dumps(self.arduinos))
            self.log("updated devices")
        else:
            self.clients.remove(self)

        self.log("disconnected")


class SetupTLS(RequestHandler):
    def get(self):
        self.write("Please accept the TLS certificate to use websockets from this device.")


def sigInt_handler(signum, frame):
    logger.info("Closing Server")

    Server.stop()

    IOLoop.current().stop()
    logger.info("Server is closed")
    sys.exit(0)


if __name__ == "__main__":
    app = HTTPServer(Application([(r"/", Server), (r"/setuptls", SetupTLS)]),
                     ssl_options={"certfile": "/etc/ssl/certs/tornado.crt", "keyfile": "/etc/ssl/certs/tornado.key"})
    app.listen(9000)
    signal.signal(signal.SIGINT, sigInt_handler)
    print(("Pin: {:05d}".format(Server.pin)))
    IOLoop.current().start()
