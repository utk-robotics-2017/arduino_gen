from appendages.util.decorators import attr_check, type_check


@attr_check
class ParsedTemplate:
    ''' A struct that holds the results of merging the appendage configs for this appendage type with its respective template

        Attributes
        ----------
        include : list
            A list of strings with each include needed by the appendage type for which this object represents
        pins : str
            A string containing the code for the pins needed by the appendages type for which this object represents
        constructors : str
            A string containing the code for the constructors needed by the appendages type for which this object represents
        setup : str
            A string containing the code to be put in setup for the appendages type for which this object represents
        loop_functions : str
            A string containing the code to be put in loop for the appendages type for which this object represents
        commands : str
            A string containing the part of the commands enumeration for the appendages type for which this object represents
        command_attaches : str
            A string containing the functions attaching the commands to callback functions for the appendages type for which this object represents
        command_functions : str
            A string containing the callback functions for the appendages type for which this object represents
        core_values : list
            A list of dict containing the config information used by RIP's core
    '''
    includes = list
    pins = str
    constructors = str
    setup = str
    loop_functions = str
    commands = str
    command_attaches = str
    command_functions = str
    extra_functions = str
    core_values = list

    def __init__(self):
        pass
