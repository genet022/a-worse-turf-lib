#!/usr/bin/python
import requests
import json
import argparse

intersection_url = 'http://localhost:5000/digitalglobe/genet/intersection'
union_url = 'http://localhost:5000/digitalglobe/genet/union'
header = {"Content-Type": "application/json", "Accept": "text/plain"}

parser = argparse.ArgumentParser(prog='rest_client.py', description='Process json file inputs.', usage='%(prog)s <intersection | union> </path/to/geojson/file>')
parser.add_argument('operation', help='Operation to perform on geojson data')
parser.add_argument('json_file', help='A file containing 2 geojson objects')

args = parser.parse_args()

with open(args.json_file) as file:
    data_json = json.load(file)

if args.operation == "intersection":
    response = requests.post(intersection_url, data=json.dumps(data_json), headers=header)
elif args.operation == "union":
    response = requests.post(union_url, data=json.dumps(data_json), headers=header)
else:
    print "Invalid operation " + args.operation
    exit()

print response.text
