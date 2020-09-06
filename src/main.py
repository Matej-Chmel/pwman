from sys import argv
from traceback import print_exc
from .commands import *

def ask_command(prompt):
	try:
		args = input(prompt).split(' ')
		call_command(args.pop(0), args)
	except Exception:
		print_exc()

def start_cmdline():
		clear()
		if stg.print_newline_on_startup:
			print()

def main():
	try:
		option = argv[1]

		if option in ['v', '--version']:
			return version()	# show version number and exit

		start_cmdline()

		# assume that the only argument is path to a file that contains plaintext
		with fopen(option) as file:
			load_plaintext(
				file.read(),
				confirm('Does the source contain header definitions?'),
				confirm('Is the source split by double newlines?'),
				True
			)
		print(
			'Plaintext was loaded successfully.\n'
			"Check your data with the 'show' command and then 'save' it, 'unload' or 'exit'.\n"
		)
	except IndexError:
		start_cmdline()

	if (
		stg.migrate_on_startup and
		Path(ctext_path := f"{data_('ciphertext.aes')}").is_file() and
		confirm('Do you want to migrate existing ciphertext.aes to a new format?')
	):	
		if load_ciphertext(ctext_path, False, False):
			save_entries()
			rename_file(
				ctext_path,
				f"{data_(datetime.now().strftime('m' + BACKUP_FORMAT[1:]))}"
			)
			print('Migrated successfully.')
		else:
			print('Migration aborted.')

	if stg.load_latest_on_startup:
		load()

	ask_command('Enter command: ')
	while this.running:
		ask_command('\nEnter command: ')

if __name__ == "__main__":
	main()
