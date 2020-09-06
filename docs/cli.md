# CLI
The program is controlled by a command-line interface so here is a list of available commands and their usage.
The text in curly brackets are identifiers for arguments. Arguments are separated by a space.

Indexes in this program are counted from 1 up.
Headers can be identified either by name or index.
`...` denotes list of values separated by spaces.

- `add`
	- Prompts user for value for each header, then it creates new entry with those values.
	- Suitable for entries with values that contain whitespace.
- `add {values...}`
	- Adds new entry with values corresponding to headers in ascending order.
- `backup`
	- Displays a menu in which user can load or delete data from a selected backup.
- `clear`
	- Clears the screen.
- `create`
	- Creates an empty backup file.
	- If another backup is already opened with unsaved changes, user will be asked to save them first.
	- Note that the file exists just in memory until you save it.
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
