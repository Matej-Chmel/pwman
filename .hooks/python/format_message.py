import re
from sys import argv
from .this import *

MESSAGE_PATH = join(REPO_DIR, argv[1])

message = None
read_local_version()

with open(MESSAGE_PATH) as file:
	message = file.read()

if re.match(r'^Version\s\d+\.\s[^\s]((.|\n)*)$', message) is None:
	# Message is not formatted correctly.
	message = f'Version {this.version}. {message}'
	print(f"Formatted message to '{message}'")
else:
	print('Message was formatted fine.')

with open(MESSAGE_PATH, 'w') as file:
	file.write(message)
