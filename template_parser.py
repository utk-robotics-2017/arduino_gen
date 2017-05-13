from appendages.util.decorators import attr_check, type_check, singleton
import re
from parsed_template import ParsedTemplate


@singleton
@attr_check
class TemplateParser:
    list_ = list

    def __new__(cls):
        return object.__new__(cls)

    def __init__(self):
        self.section_head_pattern = re.compile(r'\s*(.*)\s*{{{')
        self.include_pattern = re.compile(r'(["|<][\w.]*["|>])')
        self.local_pattern = re.compile(r'<<<([\w.]*)>>>')
        self.loop_seperated_by_pattern = re.compile(r'loop_seperated_by\([\'|\"](.+)[\'|\"]\)')
        self.core_values_pattern = re.compile(r'(.+)\s*=\s*(.+)')

    @type_check
    def parse_template(self, template_filename: str, list_: list) -> ParsedTemplate:
        self.list_ = list_
        self.setup_globals()
        self.lines = []
        # Pull file into memory
        with open(template_filename) as f:
            for line in f:
                self.lines.append(line)

        template_heirachy = {}
        self.num_lines = len(self.lines)
        # print("NUMBER OF LINES: {0:d}".format(self.num_lines))

        self.line_number = 0
        while self.line_number < self.num_lines:
            section_title, section_contents, end_line_number = self.grab_section()
            template_heirachy[section_title] = section_contents
            self.line_number = end_line_number + 1

        pt = ParsedTemplate()
        pt.includes = []
        if 'include' in template_heirachy:
            include_list = template_heirachy['include']
            for include in include_list:
                m = self.include_pattern.match(include.strip())
                if m is not None:
                    matches = m.groups()
                    if len(matches) == 1:
                        #TODO: check is m.groups() returns a tuple or list
                        # if list then replace the below line with:
                        # pt.include += matches
                        pt.includes += [matches[0]]
        pt.pins = ""
        if 'pins' in template_heirachy:
            for line in template_heirachy['pins']:
                if isinstance(line, str):
                    line = line.strip()  # Remove leading and trailing whitespace
                    if line == "":
                        continue
                    pt.pins += self.apply_globals(line) + "\n"
                # inner section
                elif isinstance(line, tuple):
                    pt.pins += self.inner_section(line)

        pt.constructors = ""
        if 'constructors' in template_heirachy:
            for line in template_heirachy['constructors']:
                if isinstance(line, str):
                    line = line.strip()  # Remove leading and trailing whitespace
                    if line == "":
                        continue
                    pt.constructors += self.apply_globals(line) + "\n"
                # inner section
                elif isinstance(line, tuple):
                    pt.constructors += self.inner_section(line)

        pt.setup = ""
        if 'setup' in template_heirachy:
            for line in template_heirachy['setup']:
                if isinstance(line, str):
                    line = line.strip()  # Remove leading and trailing whitespace
                    if line == "":
                        continue
                    pt.setup += self.apply_globals(line) + "\n"
                # inner section
                elif isinstance(line, tuple):
                    pt.setup += self.inner_section(line)

        pt.loop_functions = ""
        if 'loop_functions' in template_heirachy:
            for line in template_heirachy['loop_functions']:
                if isinstance(line, str):
                    line = line.strip()  # Remove leading and trailing whitespace
                    if line == "":
                        continue
                    pt.loop_functions += self.apply_globals(line) + "\n"
                # inner section
                elif isinstance(line, tuple):
                    pt.loop_functions += self.inner_section(line)

        pt.commands = ""
        if 'commands' in template_heirachy:
            for line in template_heirachy['commands']:
                if isinstance(line, str):
                    line = line.strip()  # Remove leading and trailing whitespace
                    if line == "":
                        continue
                    pt.commands += self.apply_globals(line) + "\n"
                # inner section
                elif isinstance(line, tuple):
                    pt.commands += self.inner_section(line)
        else:
            raise Exception("commands section not in template")

        pt.command_attaches = ""
        if 'command_attaches' in template_heirachy:
            for line in template_heirachy['command_attaches']:
                if isinstance(line, str):
                    line = line.strip()  # Remove leading and trailing whitespace
                    if line == "":
                        continue
                    pt.command_attaches += self.apply_globals(line) + "\n"
                # inner section
                elif isinstance(line, tuple):
                    pt.command_attaches += self.inner_section(line)
        else:
            raise Exception("command attaches section not in template")

        pt.command_functions = ""
        if 'command_functions' in template_heirachy:
            for line in template_heirachy['command_functions']:
                if isinstance(line, str):
                    line = line.strip()  # Remove leading and trailing whitespace
                    if line == "":
                        continue
                    pt.command_functions += self.apply_globals(line) + "\n"
                # inner section
                elif isinstance(line, tuple):
                    pt.command_functions += self.inner_section(line)
        else:
            raise Exception("command functions section not in template")

        pt.extra_functions = ""
        if 'extra_functions' in template_heirachy:
            for line in template_heirachy['extra_functions']:
                if isinstance(line, str):
                    line = line.strip()  # Remove leading and trailing whitespace
                    if line == "":
                        continue
                    pt.extra_functions += self.apply_globals(line) + "\n"
                # inner section
                elif isinstance(line, tuple):
                    pt.extra_functions += self.inner_section(line)

        pt.core_values = []
        if 'core_values' in template_heirachy:
            for index, appendage in enumerate(list_):
                d = {}
                d['label'] = appendage.label
                d['index'] = index
                d['type'] = appendage.__class__.__name__
                for line in template_heirachy['core_values']:
                    line = line.strip()  # Remove leading and trailing whitespace
                    if line == "":
                        continue
                    line = self.apply_globals(line)
                    line = self.apply_locals(line, appendage)
                    m = self.core_values_pattern.match(line)
                    if m is not None:
                        matches = m.groups()
                        if len(matches) == 2:
                            d[matches[0]] = matches[1]
                        else:
                            raise Exception("core values format not correct")
                pt.core_values.append(d)
        else:
            raise Exception("core values section not in template")


        return pt

    def setup_globals(self):
        self.global_vars = {}
        self.global_vars['length'] = len(self.list_)

    def apply_globals(self, line):
        for global_var in self.global_vars:
            if "%%%{0:s}%%%".format(global_var) in line:
                try:
                    line = line.replace("%%%{0:s}%%%".format(global_var), str(self.global_vars[global_var]))
                except:
                    raise Exception("Error could not convert global {0:s} value {} to string".format(global_var, self.global_vars[global_var]))
        return line

    def grab_section(self):
        section_contents = []
        section_head = ""
        has_section_head = False

        # print("GRABBING SECTION")

        while self.line_number < self.num_lines:
            line = self.lines[self.line_number]
            # print("\tLINE: {0:d} - {1:s}".format(self.line_number, line))
            if '{{{' in line:
                if not has_section_head:
                    m = self.section_head_pattern.match(line)
                    if m is not None:
                        matches = m.groups()
                        if len(matches) == 1:
                            section_head = matches[0]
                            has_section_head = True
                            # print("\tFOUND SECTION HEAD: {0:s}".format(section_head))
                        else:
                            raise Exception("Error reading section head on line {0:d}:{1:s}".format(self.line_number, line))
                    else:
                        raise Exception("Error reading section head on line {0:d}:{1:s}".format(self.line_number, line))
                else:
                    # print("\tFOUND INNER SECTION")
                    temp_section_head, temp_section_contents, end_line_number = self.grab_section()
                    section_contents.append((temp_section_head, temp_section_contents))
                    self.line_number = end_line_number
            elif '}}}' in line:
                if not has_section_head:
                    raise Exception("Error closing '}}}}}}' without opening '{{{{{{' on line number {0:d}".format(self.line_number))
                else:
                    # print("\tFOUND END OF SECTION")
                    return section_head, section_contents, self.line_number
            else:
                section_contents.append(line)
            self.line_number += 1
        raise Exception("Error finished file while still in section {0:s}".format(section_head))

    def inner_section(self, section):
        section_head = section[0]
        rv = ""
        if section_head == 'loop':
            for appendage in self.list_:
                for line in section[1]:
                    if isinstance(line, str):
                        line = line.strip()  # Remove leading and trailing whitespace
                        if line == "":
                            continue
                        temp = self.apply_globals(line)
                        rv += self.apply_locals(temp, appendage) + '\n'
                    # inner section
                    elif isinstance(line, tuple):
                        rv += self.inner_section(line)
        if 'loop_seperated_by' in section_head:
            m = self.loop_seperated_by_pattern.match(section_head)
            if m is not None:
                matches = m.groups()
                if len(matches) == 1:
                    for appendage in self.list_:
                        for line in section[1]:
                            if isinstance(line, str):
                                line = line.strip()  # Remove leading and trailing whitespace
                                if line == "":
                                    continue
                                temp = self.apply_globals(line)
                                rv += self.apply_locals(temp, appendage) + matches[0] +'\n'
                                # inner section
                            elif isinstance(line, tuple):
                                rv += self.inner_section(line)
                    #rv = rv[:-(len(matches[0]) + 1)] + '\n' # Remove the last separator

        return rv

    def apply_locals(self, line, appendage):
        matches = self.local_pattern.findall(line)
        locals_ = []
        if matches is not None and len(matches) > 0:
            for match in matches:
                # If match is in locals_ then we have already replaced it
                if match not in locals_:
                    dot = match.split('.')
                    value = appendage
                    for d in dot:
                        value = getattr(value, d)
                    try:
                        line = line.replace('<<<{0:s}>>>'.format(match), str(value))
                    except:
                         raise Exception("Error could not convert {} to string".format(value))
                    finally:
                        locals_.append(match)
        return line

