# Let's start
This guide will show you how to run the app and how to pass it some data.

## Running the app
First choose a way of running the app:
- If you use VS Code:
	- You can execute the [Run](../.vscode/tasks.json#L5) task to start the app.
	- If you want to pass optional arguments, execute the [Run with arguments](../.vscode/tasks.json#L15) task.
		- You will be prompted for an optional argument from a list of values.
		- You can edit the list of arguments in the [task definition](../.vscode/tasks.json#L32).
- If you can run batch or shell scripts, run one from the [run](../run/) directory.
	- You pass optional arguments to the scripts themselves which will then pass those this app.
	- You can also drag files onto the scripts.
- You can also run the [src/main.py](../src/main.py) script directly with `python -m src.main`.

## The data
There are two main ways how can user start using this app:

### Start with a clean slate
If you don't have any data that you would like to start with, just run the app without any arguments or files passed into it. Then type [`create`](cli.md#L18) as a first command. You run [any command](cli.md) now. When you try to [`exit`](cli.md#L26) the app, you will be prompted to save the file you've just created.

> Note: To load / save empty files, you don't need a password.

### Migrate existing data
To migrate existing data, save them into a file in one of these formats:

#### Tabs
Values are separated by tabs, entries are separated by a single newline. Look at an [example](../data/examples/tabs.txt).

> Note: The number of tabs doesn't matter but at least one tab is required between each two values for the same entry.

#### Double newline
Values are separated by a single newline, entries are separated by two newlines (one blank line). Look at an [example](../data/examples/double_newline.txt).

#### Formatting rules
These rules apply for all formats above:

- You can define header names in the first entry.
- Values that don't have a header name defined, will be assigned header with a default name.
- Empty values are represented by a single `#`.
- When a value starts with a `#`, prefix it with one more `#`.
- When an empty value is the last one for the entry and you use the [tabs](#tabs) format, you don't have to represent it with a `#`. You can just leave it blank.
- If your data contains tabs, you have to use the [double newline](#double-newline) format.

#### Passing the data to the app
1. Pass the absolute path to the file as a sole argument when running the app. You can drag the file onto the one of the scripts in the [run](../run/) directory to make this step easier.
2. You will be prompted for two key information:
	- Does the first entry contain the header names?
	- Do you use the double newline format?
3. If everything went well, your data is now saved in memory and not yet encrypted.
4. To encrypt your data, run the [`save`](cli.md#L48) command and provide a password.

### Continue from where you left off
When you run the app, no data is loaded. There are three ways of viewing your data:

- Type [`load`](cli.md#L39) to load the latest backup.
- Type [`backup`](cli.md#L14) to choose what backup to load.
- Type [`settings`](cli.md#L56) to display the settings menu.
	- Then change the `load_latest_on_startup` setting to True.
	- Save the settings.
	- This will run the [`load`](cli.md#L39) command on startup automatically.
