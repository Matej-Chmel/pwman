from getpass import getpass
from .cipher import decrypt, encrypt
from .this import *

def confirm(prompt):
	while True:
		result = input(f'{prompt} (y/n): ').lower()
		if result in ['y', 'yes', 'ok']:
			return True
		if result in ['n', 'no', 'nope']:
			return False
		print('Please answer yes or no.')

def choice(prompt, options: list, return_idx=False):
	print(f"""{f'{chr(10)}'.join([
		f'{idx + 1}{chr(9)}{item}' for idx, item in enumerate(options)
		])}{chr(10)}""")
	while True:
		try:
			result = input(f'{prompt}: ')
			if result in ['n', 'exit', 'cancel']:
				return None
			idx = int(result) - 1
			if return_idx:
				if not (0 <= idx < len(options)):
					raise IndexError()
				return idx
			return options[idx]
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

def load_ciphertext(path, headers: bool, new_format: bool):
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
			'Current data is not saved. Choose an option from above',
			[
				'Abort loading of new data.',
				'Save current data first then load new.',
				'Load new data without saving the old ones.'
			],
			return_idx=True
		)
		if result in [None, 0] or result == 1 and not save_entries():
			return False
	data = None
	max_length = 0
	if new_format:
		# packs are split by double newline
		# individual data are split by one newline
		packs = plaintext.split('\n\n')
		data = [
			[
				'' if item == '#' else
				item[1:] if item.startswith('#') else
				item
				for item in pack.split('\n')
			]
			for pack in packs
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
		this.headers = {
			name.replace(' ', '') if name else f'header-{idx + 1}' : idx
			for idx, name in enumerate(data.pop(0))
		}
		max_length = max(max_length, len(this.headers))
	else:
		this.headers = {}
	for idx in range(len(this.headers), max_length):
		this.headers[f'header-{idx + 1}'] = idx
	unload_entries([Entry(item, max_length) for item in data], this.headers)
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
				f"{chr(10).join(this.headers)}{chr(10)}{chr(10)}"
				f"""{f'{chr(10)}{chr(10)}'.join([
					f'{chr(10)}'.join([
						'#' if item == '' else
						f'#{item}' if item.startswith('#') else
						item
						for item in entry.data
					])
					for entry in this.entries
				])}"""
			)
		)
	backups.insert(0, join(DATA_DIR, filename))
	print('Save completed.')
	return True
