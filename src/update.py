from os import chdir as cd
from .command_structure import command
from .specific import system_call
from .this import read_version

@command('Pulls latest codebase from github.', False)
def update(args = None):
	# move into the root directory of this repository
	cd(REPO_DIR)
	old_version = read_version()
	system_call('git pull --tags origin master')
	print(
		'No updates found.' if old_version == (new_version := read_version(True))
		else f'Updated the app from version {old_version} to {new_version}.'
	)
