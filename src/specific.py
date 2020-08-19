import os
from sys import platform
from .command_structure import command

help_clear = 'Clears the screen.'

if platform.startswith('linux'):
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
