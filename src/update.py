from os import chdir as cd
from subprocess import CalledProcessError, check_output as execute
from .command_structure import *

def system_call(text, success_message):
	try:
		execute(text.split(' '))
		print(success_message)
	except CalledProcessError as e:
		print(
			f'Something went wrong.\n'
			f'Error code: {e.returncode}\n'
			f'More info: {e.output}\n'
		)

@command('Pulls latest codebase from github.', False)
def update(args = None):
	# move into the root directory of this repository
	cd(REPO_DIR)
	system_call('git pull --tags origin master')
