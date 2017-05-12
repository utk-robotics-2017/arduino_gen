from appendages.utils.decorators import attr_check, type_check, singleton
import re

@singtlon
@attr_check
class TemplateParser:
	list_ = list
	
	INCLUDE_PATTERN = re.compile(r'include\w*{\w(.*)\w*}')
	PINS_PATTERN = re.compile(r'pins\w*{\w(.*)\w*}')
	CONSTRUCTORS_PATTERN = re.compile(r'constructors\w*{\w(.*)\w*}')
	SETUP_PATTERN = re.compile(r'setup\w*{\w(.*)\w*}')
	COMMANDS_PATTERN = re.compile(r'commands\w*{\w(.*)\w*}')
	COMMAND_ATTACHES_PATTERN = re.compile(r'command_attaches\w*{\w(.*)\w*}')
	COMMAND_FUNCTIONS_PATTERN = re.compile(r'command_functions\w*{\w(.*)\w*}')
	EXTRA_FUNCTIONS_PATTERN = re.compile(r'extra_functions\w*{\w(.*)\w*}')
	CORE_VALUES_PATTERN = re.compile(r'core_values\w*{\w(.*)\w*}')

	@staticmethod
	@type_check
	def get_parsed_template(self, template_filename: str, list_: list): -> ParsedTemplate
		self.list_ = list_
		with open(template_filename) as f:
			self.template_text = f.read()

		pt = ParsedTemplate()
		pt.include = self.get_include()
		pt.pins = self.get_pins()
		pt.constructors = self.get_constructors()
		pt.setup = self.get_setup()
		pt.commands = self.get_commands()
		pt.command_attaches = self.get_command_attaches()
		pt.command_functions = self.get_command_functions()
		pt.extra_functions = self.get_extra_functions()
		pt.core_values = self.get_core_values()

		return pt

	@type_check
	def get_include(self): -> (str, None)
		m = INCLUDE_PATTERN.match(self.template_text)
		if m is None:
			return None

		matches = m.groups()
		print(matches)

	@type_check
	def get_setup(self): -> (str, None)
		m = SETUP_PATTERN.matches(self.template_text)
		if m is None:
			return None

		matches = m.groups()
		print(matches)

	@type_check
	def get_constructors(self): -> (str, None)
		m = CONSTRUCTORS_PATTERN.matches(self.template_text)
		if m is None:
			return None

		matches = m.groups()
		print(matches)

	@type_check
	def get_commands(self): -> (str, None)
		m = COMMANDS_PATTERN.matches(self.template_text)
		if m is None:
			return None

		matches = m.groups()
		print(matches)

	@type_check
	def get_command_attaches(self): -> (str, None)
		m = COMMAND_ATTACHES_PATTERN.matches(self.template_text)
		if m is None:
			return None

		matches = m.groups()
		print(matches)

	@type_check
	def get_command_functions(self): -> (str, None)
		m = COMMAND_FUNCTIONS_PATTERN.matches(self.template_text)
		if m is None:
			return None

		matches = m.groups()
		print(matches)

	@type_check
	def get_extra_functions(self): -> (str, None)
		m = EXTRA_FUNCTIONS_PATTERN.matches(self.template_text)
		if m is None:
			return None

		matches = m.groups()
		print(matches)

	@type_check
	def get_core_values(self): -> (str, None)
		m = CORE_VALUES_PATTERN.matches(self.template_text)
		if m is None:
			return None

		matches = m.groups()
		print(matches)