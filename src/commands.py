from ast import literal_eval as eval
from getpass import getpass
from cipher import decrypt, encrypt
from specific import help_clear, clear
from this import this, WrongUsage, CIPHER_PATH, PLAIN_PATH, all_encodings, encoding

actions = {}
help_strings = {}

def confirm(prompt):
	while True:
		result = input(f'{prompt} (y/n): ').lower()
		if result in ['y', 'yes', 'ok']:
			return True
		if result in ['n', 'no', 'nope']:
			return False
		print('Please answer yes or no.')

def create_password():
	while True:
		password = getpass(prompt='Create password: ')
		confirm_pwd = getpass(prompt='Confirm password: ')
		if password == confirm_pwd:
			return password
		if not confirm('Password mismatched.\nTry again?'):
			return None

def encrypt_plaintext():
	try:
		with open(PLAIN_PATH, 'r') as plain, open(CIPHER_PATH, 'w+') as cipher:
			key = create_password()
			if key is None:
				print('Plaintext was not encrypted.')
				return
			cipher.write(encrypt(key, plain.read()))
		print('Plaintext encrypted successfully.')
	except Exception as e:
		print(f'{e}\nPlaintext was not encrypted.')

def display_ciphertext():
	try:
		with open(CIPHER_PATH, 'r') as cipher:
			print(decrypt(getpass('Enter password: '), cipher.read()))
	except OSError as e:
		print(f'{e}\nCiphertext could not be opened.')
	except ValueError as e:
		print(f'Wrong password.')
	except Exception as e:
		print(e)

# decorator
def command(help_string: str):
	def wrap(action):
		actions[action.__name__] = action
		help_strings[action.__name__] = help_string
		return action
	return wrap

@command('Takes one argument - name of encoding. Changes encoding used for encrypting and decrypting files.')
def cod(args: list):
	global encoding
	if len(args) == 0:
		print(f'Current encoding is {encoding}.')
		return
	if args[0] not in all_encodings:
		raise WrongUsage(f'{args[0]} is not a valid encoding.')
	encoding = args[0]
	print(f'Encoding successfully set to {args[0]}.')

@command('Prompts user for new password and then encrypts local file named plaintext.txt and saves it as ciphertext.aes')
def enc(args: list):
	encrypt_plaintext()

@command('Exits the program.')
def exit(args: list):
	this.running = False

@command('Takes one argument - command name. Prints help string for a given command.')
def help(args: list):
	if len(args) < 1:
		print(f'Available commands:{chr(10)}{chr(10).join([name for name in actions])}')
		return
	print(help_strings[args[0]])

@command('Prompts user for password. If correct, displays encrypted message from ciphertext.aes')
def show(args: list):
	display_ciphertext()

command(help_clear)(clear)
