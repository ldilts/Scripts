#!/usr/bin/python

import socket
import sys
import requests
import json
import datetime
import time
import threading
import urllib2

# SERVER_URL = 'http://requestb.in/1lz3h7s1'
SERVER_URL = 'http://127.0.0.1:8000/log/'

# Get current time
date = datetime.datetime.now()

# Create payload data
data = {
  "log_id": 12346,
  "log_open": True,
  "log_date": str(date)
  }

# payload = json.dumps(data)

# # req = urllib2.Request(SERVER_URL, payload, {'Content-Type': 'application/json'})
# req = urllib2.Request(SERVER_URL, payload)
# f = urllib2.urlopen(req)
# response = f.read()
# f.close()

# results = requests.get(SERVER_URL, 
#               params={}, 
#               headers={'User-Agent': 'application/json})

# payload = json.dumps(data)


r = requests.post(SERVER_URL, json = data)
print "Status: ", r.status_code
print r.content