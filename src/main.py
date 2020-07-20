from commands import this, actions, clear

def main():
	clear()
	while this.running:
		try:
			args = input('Enter command: ').split(' ')
			cmdname = args.pop(0)
			actions[cmdname](args)
		except KeyError:
			print(f'Command {cmdname} not recognized.')
		except Exception as e:
			print(e)

main()
