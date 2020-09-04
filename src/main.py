from sys import argv
from .commands import *

def main():
	try:
		option = argv[1]

		if option in ['v', '--version']:
			return version()	# show version number and exit

		clear()

		# assume that the only argument is path to a file
		# that contains plaintext and encrypt it
		with fopen(option) as file:
			load_plaintext(
				file.read(),
				confirm('Does the source contain header definitions?'),
				confirm('Is the source split by double newlines?')
			)
		save_entries()
		print('Plaintext was encrypted successfully.')
	except IndexError:
		pass

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

	while this.running:
		try:
			args = input('\nEnter command: ').split(' ')
			call_command(args.pop(0), args)
		except Exception as e:
			print(e)

if __name__ == "__main__":
	main()
