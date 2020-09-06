# pwman
A command-line password manager. Well, I named it that way, but it can hold any type of data that you want to encrypt.

It's also a project on which I tried out some of the advanced Python concepts like decorators with arguments, platform specific code and subprocesses.

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

## Installation and usage
Please refer to the [docs](docs/):
- [Installation](docs/installation.md)
- [Start](docs/start.md)
- [CLI](docs/cli.md)

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
