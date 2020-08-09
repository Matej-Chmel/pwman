from os import renames as rename_file
from pathlib import Path
from sys import argv
from .commands import *

def main():
	if len(argv) > 2:
		# wrong usage
		print('Pwman expects 0 or 1 arguments but more were passed in.')
		return
	
	if len(argv) == 2 and argv[1] in ['v', '--version']:
		# show version number and exit
		version()
		return
	
	clear()

	if len(argv) == 2:
		# assume that the only argument is path to a file
		# that contains plaintext and encrypt it
		with fopen(argv[1]) as file:
			load_plaintext(
				file.read(),
				confirm('Does the source contain header definitions?'),
				confirm('Is the source split by double newlines?')
			)
		save_entries()
		print('Plaintext was encrypted successfully.')
	
	if (
		stg.migrate_on_startup and
		Path(ctext_path := f'{DATA_DIR}/ciphertext.aes').is_file() and
		confirm('Do you want to migrate existing ciphertext.aes to a new format?')
	):	
		if load_ciphertext(ctext_path, False, False):
			save_entries()
			rename_file(
				ctext_path,
				f"{DATA_DIR}/{datetime.now().strftime('m' + BACKUP_FORMAT[1:])}"
			)
			print('Migrated successfully.')
		else:
			print('Migration aborted.')

	if stg.load_latest_on_startup:
		load()

	while this.running:
		try:
			args = input('\nEnter command: ').split(' ')
			print()
			cmdname = args.pop(0)
			actions.call(cmdname, args)
		except KeyError:
			not_recognized(cmdname)
		except Exception as e:
			print(e)

if __name__ == "__main__":
	main()
