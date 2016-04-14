class generator:
    def __init__(self, sensor_list):
        self.sensor_list = sensor_list

    def add_includes(self):
        includes_set = set()
        for sensor in self.sensor_list:
            include = sensor.get_include()
            if include != "":
                includes_set.add(include)
        rv = ""
        for include in includes_set:
            rv = rv + "#include \"%s\";\n" % include
        return rv

    def add_pins(self):
        rv = ""
        for sensor in self.sensor_list:
            rv = rv + sensor.get_pins() + "\n"
        return rv

    def add_setup(self):
        return ""

    def add_constructors(self):
        rv = ""
        for sensor in self.sensor_list:
            rv = rv + sensor.get_constructor() + "\n"
        return rv

    def add_commands(self):
        return ""
