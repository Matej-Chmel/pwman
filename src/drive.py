from pathlib import Path
from pydrive.auth import GoogleAuth, AuthenticationRejected
from pydrive.drive import GoogleDrive as Drive, GoogleDriveFile as File
from .auth import gauth
from .this import data, res_, sort_backup

FOLDER_TYPE = 'application/vnd.google-apps.folder'

app_folder: File = None
drive: Drive = None

def ensure_item(title: str, mime_type=None, parents=None, trashed=False):
	query = f"title='{title}'"
	if mime_type:
		query += f" and mimeType='{mime_type}'"
	if parents:
		query += f""" and {
			' and '.join(f"'{item['id']}' in parents" for item in parents)
		}""" if type(parents) is list else f" and '{parents['id']}' in parents"
	if trashed is not None:
		query += f' and trashed={str(trashed).lower()}'

	try:
		return drive.ListFile({'q': query}).GetList()[0]
	except IndexError:
		metadata = {'title': title}
		if mime_type:
			metadata['mimeType'] = mime_type
		if parents:
			metadata['parents'] = [
				{'id': item['id']} for item in parents
			] if type(parents) is list else [{'id': parents['id']}]

		file = drive.CreateFile(metadata)
		file.Upload()
		return file

def log_into_drive():
	secrets_path = res_('client_secrets.json')

	if not Path(secrets_path).is_file():
		return print(
			"File 'res/client_secrets.json' is missing.\n"
			"Please refer to Installation section in 'README.md' in the root of this repo."
		)

	GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = secrets_path
	creds_path = res_('creds.json')

	if Path(creds_path).is_file():
		gauth.LoadCredentialsFile(creds_path)
	else:
		try:
			gauth.LocalWebserverAuth()
			gauth.SaveCredentialsFile(creds_path)
		except:
			return None

	return Drive(gauth)

def login_and_init():
	global app_folder, drive
	if drive is not None:
		return True

	if (drive := log_into_drive()) is None:
		return False

	app_data = ensure_item('AppData', FOLDER_TYPE)
	app_folder = ensure_item('pwman', FOLDER_TYPE, app_data)
	app_folder.id = app_folder['id']
	return True

def synchronize(newest_local_name=None):
	global app_folder, drive

	def download():
		with data(filename := newest_online['title'], 'w+') as file:
			file.write(newest_online.GetContentString())
		print('Newest data was downloaded to your device.')
		return filename

	def upload():
		with data(newest_local_name) as file:
			saved = drive.CreateFile({'title': newest_local_name, 'parents': [{'id': app_folder.id}]})
			saved.SetContentString(file.read())
			saved.Upload()
		return print('Your newest data was uploaded to the cloud.')

	def sortkey(file: File):
		return sort_backup(file['title'])

	online_backups = drive.ListFile({'q': f"'{app_folder.id}' in parents and trashed=false"}).GetList()

	if not online_backups:
		return upload() if newest_local_name else print('There is nothing to sync.')

	newest_online = sorted(online_backups, key=sortkey, reverse=True)[0]

	if not newest_local_name:
		return download()

	online_date = sortkey(newest_online)
	local_date = sort_backup(newest_local_name)

	if local_date == online_date:
		return print('Cloud and your device are already synchronized.')
	return upload() if local_date > online_date else download()
