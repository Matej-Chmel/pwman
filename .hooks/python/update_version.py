from base64 import b64decode
from requests import get, codes
from .this import *

REPO_URL = 'https://api.github.com/repos/Matej-Chmel/pwman'
VERSION_URL = f'{REPO_URL}/contents/res/version.txt'

try:
	request = get(REPO_URL)

	if request.status_code == codes.ok: #pylint: disable=no-member
		print('Repository is public.')
		request = get(VERSION_URL)
	else:
		# repo might be private, it doesn't exist or other error occurred
		print('Repository might be private. Reading token.')
		with open(TOKEN_PATH) as file:
			token = file.read()

		request = get(VERSION_URL, headers={'Authorization': f'token {token}'})

	if request.status_code == codes.ok: #pylint: disable=no-member
		print('Reading latest version from github.')
		this.version = int(b64decode(request.json()['content']))
	else:
		read_local_version('Repository or file not found.')

except OSError:
	read_local_version(
		'Token not found.\n'
		'Private repositories cannot be viewed without a token.'
	)

print(f'Latest version was {this.version}.')
this.version += 1

with open(VERSION_PATH, 'w') as file:
	file.write(str(this.version))

print(f'Successfully upgraded version to {this.version}.')
