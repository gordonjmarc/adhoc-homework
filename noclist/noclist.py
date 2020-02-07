#!/usr/bin/python3
import json
import requests
import hashlib
import sys
from pprint import pprint

class NocList:
	api_url_base = None
	auth_endpoint = None
	users_endpoint = None
	api_token = None
	request_retry_limit = 3
	request_timeout = 5

	def __init__(self, init_api_url_base = 'http://0.0.0.0:8888'):
		self.api_url_base = init_api_url_base
		self.auth_endpoint = '{0}/auth'.format(self.api_url_base)
		self.users_endpoint = '{0}/users'.format(self.api_url_base)

	def get_api_token(self):
		request_attempts = 0

		while request_attempts < self.request_retry_limit:
			auth_response = requests.get(self.auth_endpoint, timeout = self.request_timeout)
			if auth_response.status_code == requests.codes.ok:
				break
			request_attempts += 1

		if request_attempts >= self.request_retry_limit:
			sys.exit("auth exceeded maximum attempts: {}".format(self.request_retry_limit))

		self.api_token = auth_response.headers['Badsec-Authentication-Token']

	def get_user_list(self):
		#TODO: validate api_token is assigned and valid

		checksum_input = "{0}/users".format(self.api_token)
		checksum_output = hashlib.sha256(checksum_input.encode('utf-8')).hexdigest()
		get_users_request_headers = {'X-Request-Checksum':checksum_output} 
		request_attempts = 0

		while request_attempts < self.request_retry_limit:
			get_user_list_response = requests.get(self.users_endpoint, headers = get_users_request_headers, timeout = self.request_timeout)
			if get_user_list_response.status_code == requests.codes.ok:
					break
			request_attempts += 1

		if request_attempts >= self.request_retry_limit:
			sys.exit("get_user_list exceeded maximum attempts: {}".format(self.request_retry_limit))

		response_text = get_user_list_response.text
		response_to_parsed_array = response_text.splitlines()

		return response_to_parsed_array

	def execute(self):
		self.get_api_token()
		user_list = self.get_user_list()
		print(json.dumps(user_list))

def main():
	my_noc_list = NocList()
	my_noc_list.execute()

main()
