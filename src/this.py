from dataclasses import dataclass, asdict as dtc_asdict
from datetime import datetime
from difflib import SequenceMatcher
from json import dumps as json_str, load as json_parse
from glob import glob
from os.path import abspath, basename, dirname, join, pardir, realpath
from typing import List, Union

REPO_DIR = abspath(join(dirname(realpath(__file__)), pardir))
DATA_DIR = join(REPO_DIR, 'data')
RES_DIR = join(REPO_DIR, 'res')
BACKUP_FORMAT = 'b%d-%m-%Y_%H-%M-%S-%f.aes'
VERSION = None

def data_(filename):
	return join(DATA_DIR, filename)

def res_(filename):
	return join(RES_DIR, filename)

def data(filename, mode='r'):
	return open(data_(filename), mode, encoding='utf-8')

def fopen(path, mode='r'):
	return open(path, mode, encoding='utf-8')

def res(filename, mode='r'):
	return open(res_(filename), mode, encoding='utf-8')

def similar(a, b):
	return SequenceMatcher(None, a, b).ratio()

def sort_backup(filename) -> datetime:
	return datetime.strptime(filename, BACKUP_FORMAT)

def read_version():
	global VERSION
	if VERSION is not None:
		return VERSION
	with res('version.txt') as file:
		VERSION = file.read().rstrip('\n')

class WrongUsage(Exception):
	def __init__(self, message, cmdname=None):
		if cmdname is not None:
			message = f"{message}\nFor more information type 'help {cmdname}'."
		super().__init__(message)

class Entry:
	@staticmethod
	def sort_key(item):
		return item.ratio
	def __init__(self, data: list, max_length=None):
		if max_length is not None:
			for _ in range(max_length - len(data)):
				data.append('')
		self.data = data
		self.ratio = 0.0
	def __str__(self):
		if this.filters is None:
			return '\n'.join(self.data)
		return '\n'.join([self.data[idx] for idx in this.filters])
	def add(self, value):
		self.data.append(value)
	def change(self, header: Union[int, str], value):
		try:
			header = int(header) - 1
			self.data[header] = value
		except ValueError:
			self.data[this.headers[header]] = value
	def similar(self, search):
		if this.filters is None:
			self.ratio = max([similar(item, search) for item in self.data])
		else:
			self.ratio = max([similar(self.data[idx], search) for idx in this.filters])

@dataclass
class Settings:
	migrate_on_startup: bool = True
	load_latest_on_startup: bool = False

class this:
	entries: List[Entry] = None
	filters: List[int] = None
	headers: List[str] = None
	modified = False
	results: List[Entry] = None
	running = True
	selected: Entry = None

def unload_entries(entries=None, clear_headers=True):
	this.entries = entries
	this.filters = None
	if clear_headers:
		this.headers = None
	this.modified = False
	this.results = this.entries
	this.selected = None

backups = sorted([basename(path) for path in glob(f"{data_('b*')}")], key=sort_backup, reverse=True)
stg = Settings()
settings_keys = [key for key in dir(stg) if not key.startswith('__')]

def save_settings():
	with res('settings.json', 'w+') as file:
		file.write(json_str(dtc_asdict(stg), indent='\t', sort_keys=True))
	print('Settings saved successfully.')

try:
	with res('settings.json') as file:
		try:
			settings_dict = json_parse(file)
			for key in settings_dict:
				if hasattr(stg, key):
					setattr(stg, key, settings_dict[key])
				else:
					print(f"'{key}' is not a settings property. It was ignored.")
			del settings_dict
		except Exception:
			pass
except OSError:
	print('Settings not found. Creating default configuration.')
	save_settings()
