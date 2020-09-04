# pwman
A command-line password manager. A project on which I tried out some of the advanced Python concepts like decorators with arguments, platform specific code and subprocesses.

## Features
- Encryption method from [StackOverflow](https://stackoverflow.com/a/44212550/10732434)
- Supports multiple platforms
	- Android running the [Termux](https://play.google.com/store/apps/details?id=com.termux&hl=cs) app
	- Linux
	- OS X
	- Windows
- On each save a new backup is created
	- This way user can recover old data easily
- Sync between devices using [PyDrive](https://pypi.org/project/PyDrive/)

## Installation
1. Clone the repo.
2. Initialize the repo by running [run/init.py](run/init.py).
3. If you want to use the sync feature, follow instructions below, otherwise skip this step.
	1. Create your own Google's console Project by following this [tutorial](https://pythonhosted.org/PyDrive/quickstart.html).
	2. Move *client_secrets.json* (the file they are talking about in the tutorial) to the [res](res/) directory.
4. Run the app by following one of the options:
	1. If you use VS Code, run the [Run](.vscode/tasks.json#L5) task.
	2. If you can run batch or shell scripts, run one from the [run](run/) directory.
	3. Or run the [src/main.py](src/main.py) directly with `python -m src.main`.

## Usage
The program is controlled by a command-line interface so here is a list of available commands and their usage.
The text in curly brackets are identifiers for arguments. Arguments are separated by a space.

Indexes in this program are counted from 1 up.
Headers can be identified either by name or index.
`...` denotes list of values separated by spaces

- `add`
	- Prompts user for value for each header, then it creates new entry with those values.
	- Suitable for entries with values that contain whitespace.
- `add {values...}`
	- Adds new entry with values corresponding to headers in ascending order.
- `backup`
	- Displays a menu in which user can load or delete data from a selected backup.
- `clear`
	- Clears the screen.
- `delete {index}`
	- Deletes entry at index in the last displayed collection of entries.
- `edit {header} {value}`
	- Edit value of header for an entry that was previously selected by the `select` command.
- `exit`
	- Closes the app.
	- If there are unsaved changes, prompts user for an action.
- `filter`
	- Adds all headers to the filter.
- `filter {headers...}`
	- Sets new filter. Only values of headers in the filter are displayed or searched. The rest is hidden.
- `headers`
	- Displays names of headers for currently loaded data.
- `help`
	- Displays list of available commands.
- `help {name}`
	- Displays description for a given command.
- `load`
	- Attempts to load the latest backup and prompts the user for a password.
	- User must provide correct password to view and use the data.
- `newheader {name} {default value}`
	- Adds new header to the currently loaded data as a last header.
	- If a default value is supplied, all entries will have this value set for the new header.
	- Otherwise, an empty string will be used as a default value.
- `rename {header} {new name}`
	- Renames a header to a new name.
- `save`
	- Save currently loaded entries.
- `search {top} {term}`
	- Apply string similarity search for a given term in all entries while considering only values for filtered headers.
	- Top is the number of results displayed. 0 means all.
- `select {index}`
	- Select entry at index in the last displayed collection of entries.
	- This entry can that be affected by other commands like `edit`.
- `settings`
	- Displays the settings menu.
- `show`
	- Displays all entries but only values from filtered headers are shown.
- `sync`
	- Sync this device with the Drive.
- `unload`
	- Forgets all information about currently loaded entries and clears the screen.
- `update`
	- Calls `git pull` to update the repo to the latest version.
	- If an update is made, the changes will take effect only after restarting the app.
- `version`
	- Displays current version number.

## Optional arguments
- `v` or `--version`
	- Displays current version number and closes the app.
- path to a plaintext file
	- App prompts you for additional information about the file then it attempts to encrypt the data and create a backup file.

## Licensing

### Third-party code

#### PyDrive

Following files are licensed under the Apache License, Version 2.0:
- [src/auth.py](src/auth.py)

Full text of the license is available in the [LICENSE_PyDrive](LICENSE_PyDrive) file.

#### StackOverflow

Following files are licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License:
- [src/cipher.py](src/cipher.py)

License notices are embedded in the respective files.

### Own work

Every file that is not mentioned in the [*Third-party code*](#third-party-code) section is licensed under the Creative Commons Zero v1.0 Universal.

Full text of the license is available in the [LICENSE](LICENSE) file.
