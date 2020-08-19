from base64 import b64decode
from requests import get, codes
from .this import *

URL = (
	'https://api.github.com/repos/Matej-Chmel/'
	'pwman/contents/res/version.txt'
)

token = None

try:
	with open(TOKEN_PATH) as file:
		token = file.read()

	request = get(URL, headers={'Authorization': f'token {token}'})

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
