from datetime import datetime
from difflib import SequenceMatcher
from glob import glob
from os.path import abspath, basename, dirname, join, pardir, realpath
from typing import Dict, List, Union

REPO_DIR = abspath(join(dirname(realpath(__file__)), pardir))
DATA_DIR = join(REPO_DIR, 'data')
BACKUP_FORMAT = 'b%d-%m-%Y_%H-%M-%S-%f.aes'
MIGRATING = len(glob(f'{DATA_DIR}/ciphertext.aes')) != 0
VERSION = None

def data(filename, mode='r'):
	return open(join(DATA_DIR, filename), mode, encoding='utf-8')

def fopen(path, mode='r'):
	return open(path, mode, encoding='utf-8')

def similar(a, b):
	return SequenceMatcher(None, a, b).ratio()

def sort_backup(filename) -> datetime:
	return datetime.strptime(filename, BACKUP_FORMAT)

class WrongUsage(Exception):
	def __init__(self, message, cmdname=None):
		if cmdname is not None:
			message = f"{message}\nFor more information type 'help {cmdname}'."
		super().__init__(message)

class Entry:
	@staticmethod
	def sort_key(item):
		return item.ratio
	def __init__(self, data: list, max_length):
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

class this:
	entries: List[Entry] = None
	filters: List[int] = None
	headers: Dict[str, int] = None
	modified = False
	results: List[Entry] = None
	running = True
	selected: Entry = None

backups = sorted([basename(path) for path in glob(f'{DATA_DIR}/b*')], key=sort_backup, reverse=True)

def unload_entries(entries=None, headers=None):
	this.entries = entries
	this.filters = None
	this.headers = headers
	this.modified = False
	this.results = this.entries
	this.selected = None

with open(join(REPO_DIR, 'res', 'version.pydef')) as file:
	try:
		VERSION = int(file.read())
	except:
		VERSION = 0
