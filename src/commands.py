from os import renames as rename_file
from pathlib import Path
from .command_structure import *
from .drive import login_and_init, synchronize
from .specific import clear
from . import update

@command(
	'add [value...]\n'
	'Adds new entry.\n'
	'Values are separated by spaces.\n'
	'Missing values will be empty.\n'
	'If no values are given, user will be prompted for data in interactive mode.\n'
	'If values contain spaces, use interactive mode.'
)
def add(args: list):
	if not args:
		this.entries.append(
			Entry([input(f'Value for {header}: ') for header in this.headers])
		)
	else:
		this.entries.append(Entry(args, len(this.headers)))
	this.modified = True
	print('Entry successfully added.')

@command(
	'Prints available backup files and prompts user to choose one.\n'
	'The user can load data from the selected backup or delete it.',
	False
)
def backup(args = None):
	if not backups:
		return print('No backups available.')
	while True:
		filename, idx = choice(
			"Choose a backup file by a number on the left or type 'exit' to leave the menu.\n",
			backups, ChoiceReturnType.option_and_index
		)
		if filename is None:
			return print('No backup file chosen. Exited the menu.')
		print(f'File {filename} selected.')
		option = choice(
			'Select an option',
			['Load', 'Delete', 'Cancel'],
			ChoiceReturnType.index
		)
		if option in [None, 2]:
			# cancel
			print('Operation cancelled.')
			continue
		if option == 1:
			# delete
			# ensure that 'trash' folder exists
			Path(data_('trash')).mkdir(parents=True, exist_ok=True)
			# move selected file to trash
			rename_file(
				data_(filename),
				join(DATA_DIR, 'trash', filename)
			)
			del backups[idx]
			print("Selected file was moved to the app's trash folder.")
			continue
		# load
		return print(
			'Data loaded successfully.'
			if load_ciphertext(data_(filename))
			else 'Operation aborted.')

@command(
	'Creates an empty backup file.\n'
	'If another backup is already opened with unsaved changes, you will be asked to save them first.',
	False
)
def create(args = None):
	if this.modified:
		result = choice(
			'Unsaved changes were detected. Choose what to do',
			[
				"Don't create a new backup.",
				'Save first then create a new backup.',
				'Create a new backup without saving the previous one.'
			], ChoiceReturnType.index)
		if result in [None, 0]:
			return print('Operation aborted.')
		if result == 1:
			save_entries()
	unload_entries([], modified=True)
	print('New backup created.')

@command(
	'delete [index]\n'
	'Deletes entry at index in search results.\n'
	"If index is not given, deletes entry selected by the 'select' command."
)
def delete(args: list):
	if not args:
		if this.selected is None:
			raise WrongUsage('No entry is selected.', 'delete')
		this.entries.remove(this.selected)
	else:
		try:
			this.entries.remove(this.results[int(args[0]) - 1])
		except IndexError:
			raise WrongUsage(f'Entry number {args[0]} not found. Maximum index is {len(this.results)}.')
		except ValueError:
			raise WrongUsage(f"'{args[0]} could not be converted to integer.'", 'delete')
	this.modified = True
	print('Entry successfully deleted.')

@command(
	'edit __header-name-or-index__ __new value__\n'
	"Edits data of the entry selected by 'select' command."
)
def edit(args: list):
	if this.selected is None:
		raise WrongUsage('No entry is selected.', 'edit')
	if len(args) < 1:
		raise WrongUsage('Header name or index is required argument.', 'edit')
	header = args.pop(0)
	value = ' '.join(args)
	this.selected.change(header, value)
	this.modified = True
	print('Entry successfully edited.')

@command('Exits the program.', False)
def exit(args = None):
	if this.modified:
		result = choice(
			'Unsaved changes were detected. Choose what to do',
			[
				"Don't exit.",
				'Save first then exit.',
				'Exit without saving.'
			], ChoiceReturnType.index)
		if result in [None, 0] or result == 1 and not save_entries():
			return print('Still running.')
	this.running = False

@command(
	'filter [header...]\n'
	'Sets filters that affect other commands.\n'
	'Empty filter means show all headers.'
)
def filter(args: list):
	if not args:
		this.filters = None
		return print('Filters set to all headers.')
	missing_header = next((header for header in args if header not in this.headers), None)
	if missing_header is not None:
		raise WrongUsage(f'Header {missing_header} is missing.', 'filter')
	this.filters = [this.headers.index(item) for item in args]
	print('Filters set successfully.')

@command('Prints current headers.')
def headers(args = None):
	print(' '.join(this.headers) if this.headers else "No headers exist.\nYou can add them with the 'newheader' command.")

@command(
	'help __command-name__\n'
	'Prints help string for a given command.',
	False
)
def help(args: list):
	if len(args) < 1:
		return print(f'Available commands:{ENDL}{ENDL.join(sorted([name for name in actions]))}')
	try:
		print_help(args[0])
	except KeyError:
		not_recognized(args[0])

@command(
	'Attempts to load data from latest backup file.',
	False
)
def load(args = None):
	if not backups:
		return print('No backups available.')
	print(
		'Data loaded successfully.'
		if load_ciphertext(data_(backups[0]))
		else 'Operation aborted.'
	)

@command(
	'newheader __name__ [default-value]\n'
	'Adds a new header to all loaded entries '
	'with default value or empty string.'
)
def newheader(args: list):
	if len(args) < 1:
		raise WrongUsage('Command takes at least one argument.', 'add')
	name = args.pop(0)
	value = ' '.join(args)
	if name in this.headers and confirm(f'Overwrite all values in header {name}?'):
		for item in this.entries:
			item.change(name, value)
		print(f'Values for header {name} changed successfully.')
	else:
		for item in this.entries:
			item.add(value)
		this.headers.append(name)
		print(f'New header {name} successfully added.')
	this.modified = True

@command(
	'rename __header-name-or-idx__ __new-name__\n'
	'Renames specified header.'
)
def rename(args: list):
	if len(args) != 2:
		raise WrongUsage('Command takes exactly two arguments.', 'rename')
	header = args[0]
	new_name = args[1]
	try:
		idx = int(header) - 1
		# index was passed
		try:
			old_name = this.headers[idx]
			this.headers[idx] = new_name
			print(f'Header {old_name} successfully renamed to {new_name}.')
		except IndexError:
			raise WrongUsage(f'Header number {idx + 1} not found. Maximum index is {len(this.headers)}')
	except ValueError:
		# name was passed
		try:
			this.headers[this.headers.index(header)] = new_name
			print(f'Header {header} successfully renamed to {new_name}.')
		except ValueError:
			raise WrongUsage(f'Header {header} not found.')
	this.modified = True

@command('Encrypts and saves data into a new file.')
def save(args = None):
	save_entries()

@command(
	'search __top__ __string__\n'
	'Searches data that satisfies filters for a similarity match.\n'
	'Argument top specifies how many results to show.\n'
	'0 means all.'
)
def search(args: list):
	if len(args) < 2:
		raise WrongUsage('Command takes at least two arguments.', 'search')
	top = None
	try:
		top = int(args[0])
	except ValueError:
		return print(f'{args[0]} could not be converted to an integer.')
	args.pop(0)
	search = ' '.join(args)
	for item in this.entries:
		item.similar(search)
	this.results = sorted(this.entries, key=Entry.sort_key, reverse=True)
	top = len(this.results) if top == 0 else top
	print('\n\n'.join(str(item) for item in this.results[:top]))

@command(
	'select __index__\n'
	'Selects an entry from search results '
	"to be used with the other commands like 'edit'."
)
def select(args: list):
	if len(args) != 1:
		raise WrongUsage('Command takes exactly one argument.', 'select')
	try:
		arg_idx = int(args[0])
		this.selected = this.results[arg_idx - 1]
		print('Selection was successful.')
	except IndexError:
		print(f'Index {arg_idx} is not accessible. Maximum index is {len(this.results)}.')
	except ValueError:
		print(f'{args[0]} could not be converted to an integer.')

@command('Shows settings menu.', False)
def settings(args = None):
	global stg
	while True:
		option, idx = choice(
			'Choose one of the flags in lowercase to change it or '
			'select a command in uppercase.\n'
			'Use number to the left of your selected option',
			settings_keys + ['SAVE', 'RESTORE DEFAULT SETTINGS', 'EXIT'],
			ChoiceReturnType.option_and_index,
			[getattr(stg, key) for key in settings_keys]
		)
		if idx in [None, len(settings_keys) + 2]:
			# exit
			return
		if idx == len(settings_keys):
			# save
			return save_settings()
		if idx == len(settings_keys) + 1:
			# restore
			stg = Settings()
			print('Settings were restored to default values but they are not saved yet.\n')
		else:
			# flag was selected
			value = confirm(
				'Choose value for the setting', 'on/off',
				['on', 't', 'true'], ['off', 'f', 'false']
			)
			setattr(stg, option, value)
			print('Setting changed successfully.\n')

@command(
	'Removes search results and '
	'displays loaded data that satisfies set filters.'
)
def show(args = None):
	if not this.entries:
		return print('No entries exist.')
	this.results = this.entries
	print('\n\n'.join(f'{idx + 1}\n{item}' for idx, item in enumerate(this.entries)))

@command('Synchronizes this device and the cloud.', False)
def sync(args = None):
	if not login_and_init():
		return print('Login into cloud aborted.')
	if this.modified and confirm('Unsaved changes detected. Would you like to save them first?') and not save_entries():
		return
	if result := synchronize(backups[0] if backups else None):
		backups.insert(0, result)
		if confirm('Do you want to load the latest data?'):
			load()

@command('Forgets decrypted data.')
def unload(args = None):
	clear()
	unload_entries()
	print('Data was unloaded.')

@command('Prints current version of the program.', False)
def version(args = None):
	print(f'Current version: {read_version()}')
