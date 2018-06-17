#!/usr/bin/python
import requests
import json

url = 'http://localhost:5000/digitalglobe/genet'
data = { "id": "3", "description": "cat", "title": "Steve"}
data_json = json.dumps(data)

payload = {"json_payload": data_json}
header = {"Content-Type": "application/json", "Accept": "text/plain"}

response = requests.post(url, data=data_json, headers=header)
print response.text
response = requests.get(url)
print response.text
response = requests.delete(url + '/3')
print response.text
response = requests.get(url)
print response.text
