from .logic import *

actions = {}

def call_command(name, args: list):
	print()
	try:
		cmd = actions[name]
		if cmd[2] and this.entries is None:
			print(
				f'Command {name} requires data to be decrypted first.\n'
				"Try commands 'load' or 'backup' first."
			)
		else:
			cmd[0](args)
	except KeyError:
		not_recognized(name)

# decorator
def command(help_string: str, requires_loaded_entries=True):
	def wrapped(action):
		actions[action.__name__] = (action, help_string, requires_loaded_entries)
		return action
	return wrapped

def not_recognized(cmdname):
	print(f"Command '{cmdname}' not recognized.\nFor list of available commands type 'help'.")

def print_help(command_name):
	print(actions[command_name][1])
