# Installation
1. Clone the repo.
2. Initialize the repo by running [run/init.py](../run/init.py).
3. If you want to use the sync feature, follow instructions below, otherwise skip this step.
	1. Create your own Google's console Project by following this [tutorial](https://pythonhosted.org/PyDrive/quickstart.html).
	2. Move *client_secrets.json* (the file they are talking about in the tutorial) to the [res](../res/) directory.
4. Run the app by following one of the options:
	1. If you use VS Code, run the [Run](../.vscode/tasks.json#L5) task.
	2. If you can run batch or shell scripts, run one from the [run](../run/) directory.
	3. Or run the [src/main.py](../src/main.py) directly with `python -m src.main`.

> Note: All paths mentioned start in the root folder of this repo.
