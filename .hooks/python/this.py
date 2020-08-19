from os.path import *

REPO_DIR = abspath(join(dirname(realpath(__file__)), pardir, pardir))
TOKEN_PATH = join(REPO_DIR, '.hooks', '.token')
VERSION_PATH = join(REPO_DIR, 'res', 'version.txt')

class this:
	version = None

def read_local_version(reason=None):
	if reason is not None:
		print(f'{reason}\nReading latest version from local file.')
	try:
		with open(VERSION_PATH) as file:
			this.version = int(file.read())
	except OSError:
		print('File res/version.txt not found. Assumed version 0.')
		this.version = 0
	except ValueError:
		print('File content could not be converted to an integer. Assumed version 0.')
		this.version = 0
