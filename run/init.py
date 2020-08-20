from os import chdir as cd
from os.path import abspath, dirname, join, pardir, realpath
import platform
from subprocess import CalledProcessError, check_output as execute
from sys import exit

# Introduce ourselves.
print('Initializing pwman...')

# Get root directory of this repository.
REPO_DIR = abspath(join(dirname(realpath(__file__)), pardir))

# And move there.
cd(REPO_DIR)

os_name = platform.system().lower()
python = 'py' if os_name.startswith('win') else 'python'
requirements_path = join(
	REPO_DIR,
	'run',
	f"{'win10_' if os_name.startswith('win') and platform.release() == '10' else ''}requirements.txt"
)

def command(text, success_message):
	try:
		execute(text.split(' '))
		print(success_message)
	except CalledProcessError as e:
		print(
			f'Something went wrong.\n'
			f'Error code: {e.returncode}\n'
			f'More info: {e.output}\n'
		)
		exit(1)

def main():
	# Let's tell git to look for hooks in our custom hooks directory.
	command(
		'git config core.hooksPath .hooks',
		'Hooks were configured successfully.'
	)
	
	# Install missing packages.
	command(
		f'{python} -m pip install -r {requirements_path} --user',
		'Completed setup of packages.'
	)

	# If we are not on Linux, our job is completed.
	if not os_name.startswith('linux'):
		return

	# If we are on Linux, we have to grant execute permissions to each hook.
	from glob import glob
	from os import stat, chmod
	from stat import S_IEXEC as EXECUTE_PERMISSION

	# List files without extension. Those are the hooks.
	hooks = [file for file in glob(f'{REPO_DIR}/.hooks/*') if '.' not in file]

	# Add execute permission to a list of already granted permissions.
	for file in hooks:
		chmod(file, stat(file).st_mode | EXECUTE_PERMISSION)

	print('Permissions were granted to all hooks successfully.')

main()
