from enum import Enum
from getpass import getpass
from itertools import zip_longest
from .cipher import decrypt, encrypt
from .this import *

# f-string escaped characters
ENDL = '\n'
TAB = '\t'

class ChoiceReturnType(Enum):
	option = 0
	index = 1
	option_and_index = 2
	value = 3

def confirm(
	prompt: str, hint='y/n',
	options_true: list = None, options_false: list = None
):
	if options_true is None:
		options_true = ['y', 'yes', 'ok']
	if options_false is None:
		options_false = ['n', 'no', 'nope']
	while True:
		selected = input(f'{prompt} ({hint}): ').lower()
		if selected in options_true:
			return True
		if selected in options_false:
			return False
		print(f'Please choose an available option ({hint}).')

def choice(
	prompt, options: list, return_type = ChoiceReturnType.option, values: list = None
):
	if values is None:
		print(f"""{f'{ENDL}'.join([
			f'{idx + 1}{TAB}{item}' for idx, item in enumerate(options)
			])}{ENDL}"""
		)
	else:
		print(f"""{f'{ENDL}'.join([
			f'{idx + 1}{TAB}{option}{TAB}{value}'
			for idx, (option, value) in enumerate(
				zip_longest(options, values, fillvalue='')
			)])}{ENDL}"""
		)
	while True:
		try:
			result = input(f"{prompt}{'>>> ' if prompt[-1] == ENDL else ': '}")
			if result in ['n', 'exit', 'cancel']:
				if return_type == ChoiceReturnType.option_and_index:
					return None, None
				return None
			idx = int(result) - 1
			if return_type == ChoiceReturnType.option:
				return options[idx]
			if return_type == ChoiceReturnType.index:
				if not (0 <= idx < len(options)):
					raise IndexError()
				return idx
			if return_type == ChoiceReturnType.option_and_index:
				return options[idx], idx
			return values[idx]
		except ValueError:
			print(f'{result} could not be converted to integer.')
		except IndexError:
			print(f'{result} is not a valid index.\nList is indexed from 1.\nMaximum index is {len(options)}.')

def create_password():
	while True:
		password = getpass(prompt='Create password: ')
		confirm_pwd = getpass(prompt='Confirm password: ')
		if password == confirm_pwd:
			return password
		if not confirm('Password mismatched.\nTry again?'):
			return None

def load_ciphertext(path, headers = True, new_format = True):
	source: str = None
	with fopen(path) as file:
		source = file.read()
	while True:
		try:
			return load_plaintext(
				decrypt(getpass('Enter password: '), source),
				headers,
				new_format
			)
		except ValueError:
			if not confirm('Wrong password.\nTry again?'):
				return False

def load_plaintext(plaintext: str, headers: bool, new_format: bool):
	if this.modified:
		result = choice(
			'Current data is not saved. Choose one from the options above',
			[
				'Abort loading of new data.',
				'Save current data first then load new.',
				'Load new data without saving the old ones.'
			],
			ChoiceReturnType.index
		)
		if result in [None, 0] or result == 1 and not save_entries():
			return False
	data = None
	max_length = 0
	if new_format:
		# packs are split by double newline
		# individual data are split by one newline
		data = [
			[
				'' if item == '#' else
				item[1:] if item.startswith('#') else
				item
				for item in pack.split('\n')
			]
			for pack in plaintext.split('\n\n')
			if any(pack)
		]
	else:
		# packs are split by newline
		# individual data are split by one or more tabs
		packs = plaintext.split('\n')
		data = [item.split('\t') for item in packs]
		data = [
			[
				'' if item == '#' else
				item[1:] if item.startswith('#') else
				item
				for item in pack
				if item
			]
			for pack in data
		]
	data = [item for item in data if item]
	max_length = max([len(item) for item in data])
	if headers:
		# first pack contains header names
		this.headers = [
			name.replace(' ', '') if name else f'header-{idx + 1}'
			for idx, name in enumerate(data.pop(0))
		]
		max_length = max(max_length, len(this.headers))
	else:
		this.headers = {}
	# Assign default name to missing headers
	for idx in range(len(this.headers), max_length):
		this.headers.append(f'header-{idx + 1}')
	unload_entries([Entry(item, max_length) for item in data], False)
	return True

def save_entries():
	key = create_password()
	if key is None:
		print('Nothing was saved.')
		return False
	filename = datetime.now().strftime(BACKUP_FORMAT)
	with data(filename, 'w+') as file:
		file.write(
			encrypt(
				key,
				f"{ENDL.join(this.headers)}{ENDL}{ENDL}"
				f"""{f'{ENDL}{ENDL}'.join([
					f'{ENDL}'.join([
						'#' if item == '' else
						f'#{item}' if item.startswith('#') else
						item
						for item in entry.data
					])
					for entry in this.entries
				])}"""
			)
		)
	backups.insert(0, filename)
	this.modified = False
	print('Save completed.')
	return True
