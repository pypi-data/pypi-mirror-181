from libraryArsein.encoder import encoderjson
import json
from json import dumps

class meghdar:
	def __init__(self,auth):
		self.Auth = auth
		self.enc = encoderjson(auth)

	def return_json(self,Json):
		return dumps({"api_version":"5","auth": self.Auth,"data_enc":self.enc.encrypt(dumps(Json))})
