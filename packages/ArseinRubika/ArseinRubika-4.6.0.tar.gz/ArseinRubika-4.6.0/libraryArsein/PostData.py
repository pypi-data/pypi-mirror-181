import aiohttp
import libraryArsein.encoder
from libraryArsein.encoder import encoderjson
import json
from json import dumps, loads


async def http(s,auth,js):
	enc = encoderjson(auth)
	async with aiohttp.ClientSession() as session:
		async with session.post(s, data = dumps({"api_version":"5","auth": auth,"data_enc":enc.encrypt(dumps(js))}) , headers = {'Content-Type': 'application/json'}) as response:
			Post =  await response.text()
			return Post


async def httpfiles(s,dade,head):
	async with aiohttp.ClientSession() as session:
		async with session.post(s, data = dade  , headers = head) as response:
			Post =  await response.text()
			return Post
