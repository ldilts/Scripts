#!/usr/bin/python

import requests
import json
import datetime

'''Requests '''
# r = requests.get('https://api.github.com/events')
# r.json()
# 
# print r.text
# print r.status_code

'''Json'''
# date = datetime.datetime.now()
# 
# data = [ {
#   "id": 1234,
#   "open": True,
#   "datetime": {
#     "second": date.second,
#     "minute": date.minute,
#     "hour": date.hour,
#     "day": date.day,
#     "month": date.month,
#     "year": date.year
#   }
# } ]
# 
# data_string = json.dumps(data)
# print 'ENCODED:', data_string
# 
# decoded = json.loads(data_string)
# print 'DECODED:', decoded
# 
# print 'ORIGINAL:', type(data[0]['id'])
# print 'DECODED :', type(decoded[0]['id'])

'''Both'''

date = datetime.datetime.now()
open = False
id = 1234

data = [ {
  "id": id,
  "open": open,
  "datetime": {
    "second": date.second,
    "minute": date.minute,
    "hour": date.hour,
    "day": date.day,
    "month": date.month,
    "year": date.year
  }
} ]

payload = json.dumps(data)


r = requests.post("http://httpbin.org/post", data = payload)
print "Status: ", r.status_code
print r.content

print "That was so much fun!"


