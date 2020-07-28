from sys import argv
from .commands import *

def main():
	clear()
	if len(argv) == 2:
		if argv[1] in ['v', '--version']:
			version()
			return

		# encrypt passed plaintext
		with fopen(argv[1]) as file:
			load_plaintext(
				file.read(),
				confirm('Does the source contain header definitions?'),
				confirm('Is the source split by double newlines?')
			)
		save_entries()
		print('Plaintext was encrypted successfully.')

	if MIGRATING and confirm('Do you want to migrate existing ciphertext.aes to new format?'):
		# migrate old ciphertext.aes to new format
		if load_ciphertext(f'{DATA_DIR}/ciphertext.aes', False, False):
			save_entries()
			print('Migrated successfully.')
		else:
			print('Migration aborted.')

	while this.running:
		try:
			args = input('\nEnter command: ').split(' ')
			print()
			cmdname = args.pop(0)
			actions.call(cmdname, args)
		except KeyError:
			print(f"Command {cmdname} not recognized.\nFor list of available commands type 'help'.")
		except Exception as e:
			print(e)

if __name__ == "__main__":
	main()
