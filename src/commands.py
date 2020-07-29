from .logic import *
from .specific import help_clear, clear

class CommandDict(dict):
	def __init__(self):
		super().__init__()
	def call(self, command_name, args):
		cmd = self[command_name]
		if cmd[2] and this.entries is None:
			print(
				f'Command {command_name} requires data to be decrypted first.\n'
				"Try commands 'load' or 'backup' first."
			)
		else:
			cmd[0](args)
	def print_help(self, command_name):
		print(self[command_name][1])

actions = CommandDict()

# decorator
def command(help_string: str, requires_loaded_entries=True):
	def wrap(action):
		actions[action.__name__] = (action, help_string, requires_loaded_entries)
		return action
	return wrap

@command(
	'add [value...]\n'
	'Adds new entry.\n'
	'Values are separated by tabs.\n'
	'Missing values will be empty.\n'
	'If no values are given, user will be prompted for data in interactive mode.\n'
	'If values contain spaces, use interactive mode.'
)
def add(args: list):
	if not len(args):
		this.entries.append(
			Entry([input(f'Value for {header}: ') for header in this.headers])
		)
	else:
		this.entries.append(
			Entry(args, len(this.headers))
		)
	print('Entry successfully added.')

@command(
	'Prints available backup files and '
	'provides choice of loading data from backup.',
	False)
def backup(args: list, latest=False):
	if len(backups) == 0:
		print('No backups available.')
		return
	filename = None
	if latest:
		filename = backups[0]
	else:
		filename = choice('Choose backup file', backups)
		if filename is None:
			print('No backup file choosen. Operation aborted.')
			return
	print(
		'Data loaded successfully.'
		if load_ciphertext(join(DATA_DIR, filename), True, True)
		else 'Operation aborted.')

@command(
	'edit __header-name-or-index__ __new value__\n'
	"Edits data of the entry selected by 'select' command.")
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
def exit(args: list):
	if this.modified:
		result = choice(
			'Unsaved changes were detected. Choose what to do',
			[
				"Don't exit.",
				'Save first then exit.',
				'Exit without saving.'
			], return_idx=True)
		if result in [None, 0] or result == 1 and not save_entries():
			print('Still running.')
			return
	this.running = False

@command(
	'filter [header...]\n'
	'Sets filters that affect other commands.\n'
	'Empty filter means show all headers.')
def filter(args: list):
	if not len(args):
		this.filters = None
		print('Filters set to all headers.')
		return
	missing_header = next((header for header in args if header not in this.headers), None)
	if missing_header is not None:
		raise WrongUsage(f'Header {missing_header} is missing.', 'filter')
	this.filters = [this.headers[item] for item in args]
	print('Filters set successfully.')

@command('Prints current headers.')
def headers(args: list):
	print(' '.join(this.headers))

@command(
	'help __command-name__\n'
	'Prints help string for a given command.',
	False)
def help(args: list):
	if len(args) < 1:
		print(f'Available commands:{chr(10)}{chr(10).join(sorted([name for name in actions]))}')
		return
	try:
		actions.print_help(args[0])
	except KeyError:
		print(f"Command {args[0]} not recognized.\nFor list of available commands type 'help'.")

@command(
	'Attempts to load data from latest backup file.',
	False)
def load(args: list):
	backup(args, True)

@command(
	'newheader __name__ [default-value]\n'
	'Adds a new header to all loaded entries '
	'with default value or empty string.')
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
		this.headers[name] = len(this.headers)
		print(f'New header {name} successfully added.')
	this.modified = True

@command(
	'rename __header-name-or-idx__ __new-name__\n'
	'Renames specified header.')
def rename(args: list):
	if len(args) != 2:
		raise WrongUsage('Command takes exactly two arguments.', 'rename')
	header = args[0]
	new_name = args[1]
	try:
		# index was passed
		header = int(header) - 1
		reversed_headers = dict(zip(this.headers.values(), this.headers.keys()))
		try:
			header_name = reversed_headers[header]
			this.headers[new_name] = this.headers.pop(header_name)
			print(f'Header {header_name} successfully renamed to {new_name}.')
		except KeyError:
			raise WrongUsage(f'Header number {header + 1} not found.')
	except ValueError:
		# name was passed
		try:
			this.headers[new_name] = this.headers.pop(header)
			print(f'Header {header} successfully renamed to {new_name}.')
		except KeyError:
			raise WrongUsage(f'Header {header} not found.')

@command('Encrypts and saves data into a new file.')
def save(args: list):
	save_entries()

@command(
	'search __top__ __string__\n'
	'Searches data that satisfies filters for a similarity match.\n'
	'Argument top specifies how many results to show.\n'
	'0 means all.')
def search(args: list):
	if len(args) < 2:
		raise WrongUsage('Command takes at least two arguments.', 'search')
	top = None
	try:
		top = int(args[0])
	except ValueError:
		print(f'{args[0]} could not be converted to an integer.')
		return
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
	"to be used with the 'edit' command.")
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

@command(
	'Removes search results and '
	'displays loaded data that satisfies set filters.')
def show(args: list):
	this.results = this.entries
	print('\n\n'.join(f'{idx + 1}\n{item}' for idx, item in enumerate(this.entries)))

@command('Forgets decrypted data.')
def unload(args: list):
	clear()
	unload_entries()
	print('Data was unloaded.')

@command('Prints current version of the program.', False)
def version(args: list = None):
	print(f'Current version: {VERSION}')

command(help_clear, False)(clear)
