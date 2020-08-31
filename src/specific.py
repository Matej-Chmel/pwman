import os
from sys import platform
from .command_structure import command

def system_call(text, success_message=None, alt=None, shell=False):
	def display_cmd(text):
		if type(text) is list:
			text = ' '.join(text)
		return f'{text[:cmd_width]}...' if len(text) > 30 else text
	try:
		output = (
			Popen(text, shell=True, stderr=PIPE, stdin=PIPE, stdout=PIPE).communicate()[0] if shell
			else check_output(text.split() if type(text) is str else text)
		)
		if success_message is not None:
			print(success_message)
		return output.decode()
	except CalledProcessError as e:
		if alt is not None:
			print(f"Command {text} didn't work, trying an alternative.")
			return system_call(alt, success_message)
		print(
			f"Something went wrong when executing:{N}"
			f"{display_cmd(text)}{N}{N}"
			f'Error code: {e.returncode}{N}'
			f'Output: {e.output.decode()}'
		)
	except FileNotFoundError:
		print(f"The command:{N}{display_cmd(text)}{N}doesn't work without a shell.")
	exit(1)

IS_TERMUX = False
help_clear = 'Clears the screen.'

if platform.startswith('linux'):
	IS_TERMUX = (
		system_call('uname -o').strip() == 'Android' and
		bool(system_call('command -v termux-open-url', shell=True))
	)
	def clear(args = None):
		os.system('clear')
elif platform == 'win32':
	def clear(args = None):
		os.system('cls')
elif platform == 'darwin':
	import subprocess as sp
	def clear(args = None):
		_ = sp.call('cls', shell=True)
else:
	help_clear = 'Prints bunch of newlines. Your target platform is not listed in the code.'
	def clear(args = None):
		print(24 * '\n')

command(help_clear, False)(clear)
