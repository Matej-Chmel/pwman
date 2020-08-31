'''
Authentication process that differs for devices running Termux.

This file is licensed under the Apache License, Version 2.0.
Full text is available in the ../LICENSE_PyDrive file.
'''

import socket
from pydrive.auth import AuthenticationError, CheckAuth, ClientRedirectHandler, ClientRedirectServer, GoogleAuth
from .logic import ENDL
from .specific import IS_TERMUX, system_call

if IS_TERMUX:
	class TermuxGoogleAuth(GoogleAuth):
		@CheckAuth
		def LocalWebserverAuth(self, host_name='localhost', port_numbers=None):
			if port_numbers is None:
	  			port_numbers = [8080, 8090]

			for port in port_numbers:
				try:
					httpd = ClientRedirectServer((host_name, port), ClientRedirectHandler)
					self.flow.redirect_uri = f'http://{host_name}:{port}/'
					break
				except socket.error:
					print(
						'Failed to start a local web server. Please check your firewall\n'
						'settings and locally running programs that may be blocking or\n'
						'using configured ports. Default ports are 8080 and 8090.'
					)
					raise AuthenticationError()

			authorize_url = self.GetAuthUrl()
			system_call(
				f'termux-open-url {authorize_url}',
				f'Your browser has been opened to visit:{ENDL}{ENDL}{authorize_url}{ENDL}'
			)
			httpd.handle_request()

			if 'error' in httpd.query_params:
				print('Authentication request was rejected')
				raise AuthenticationRejected('User rejected authentication')
			if 'code' in httpd.query_params:
				return httpd.query_params['code']
			print(
				"Failed to find 'code' in the query parameters of the redirect."
				'Try command-line authentication'
			)
			raise AuthenticationError('No code found in redirect')

	gauth = TermuxGoogleAuth()
else:
	gauth = GoogleAuth()
