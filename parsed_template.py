from appendages.util.decorators import attr_check, type_check


@attr_check
class ParsedTemplate:
    includes = list
    pins = str
    constructors = str
    setup = str
    loop = str
    commands = str
    command_attaches = str
    command_functions = str
    core_values = list

    def __init__(self):
        pass

    @type_check
    def get_includes(self) -> list:
        pass

    @type_check
    def get_pins(self) -> str:
        pass

    @type_check
    def get_constructors(self) -> str:
        pass

    @type_check
    def get_setup(self) -> str:
        pass

    @type_check
    def get_loop(self) -> str:
        pass

    @type_check
    def get_commands(self) -> str:
        pass

    @type_check
    def get_command_attaches(self) -> str:
        pass

    @type_check
    def get_command_functions(self) -> str:
        pass

    @type_check
    def get_extra_functions(self) -> str:
        pass

    @type_check
    def get_core_values(self) -> list:
        pass
