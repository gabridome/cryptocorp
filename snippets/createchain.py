#!/usr/bin/python
# -*- coding: utf-8 -*-
#http://ms-brainwallet.org/#bip32 is a site where you can generate a bunch of keys for testing
# You must first generate at least 2 extended bip32 Master key pairs (private and pubblic)
# 
# the following are just examples on how they should look like:
#msk1 = "xprv9s21ZrQH143K3YWKyCt7zyDZdbWHRLxT8u66rUg1nCKgVShH3ELECXpnsaCgSMfRv3GpxT4cLH8Xy1YvPqYJDF2QagYya8oa7Hb7YQgyZgN"
#mpk1 = "xpub661MyMwAqRbcG2ao5ER8N7AJBdLmpogJW81hes5dLXrfNF2RameUkL9GisfAt3CeqoE7oY8RdKwHKcYAZUb4MtZhnPi4ABRP185iYCrrxwT"

#msk2 = "xprv9s21ZrQH143K3TBwt5FDxr4Hse7HpxyBMiEvRa3RHKrWCqWZ9dWVfTzpirNWjYWiQQuQzYWAQsXD4PbooL3dv6wBNVEjkVH83FRFeMJCk14"
#mpk2 = "xpub661MyMwAqRbcFwGQz6nEKz12RfwnERh2iwAXDxT2qfPV5dqhhApkDGKJa9hrNJXEnCjR6aXmuPrAanjeSSh6Qpo2sFCpVqDucNxon7z4un7"
# Generate yours and put them below

# Extended Master Private key number 1:
msk1 = "xprv..."
mpk1 = "xpub..."

# Extended Master Private key number 2:

msk2 = "xprv..."
mpk2 = "xpub..."

from pycoin.key import *
from pycoin.key.BIP32Node import *
from pycoin.serialize import b2h


import uuid
import binascii
rulesetId = "default"
walletAgent = "HDM-2.0-cc-011"
keys = [mpk1, mpk2]
asset = "BTC"
period = 60
value = 0.0
delay = 60
phone = "+393489992529"
email = "gabridome@fastmail.fm"

payload =  {"rulesetId": rulesetId, "walletAgent": walletAgent, "keys": keys, "parameters": {"levels": [{"asset": asset, "period": period, "value": value}, {"delay": delay, "calls": ["phone","email"]}]},"pii": { "email": email, "phone": phone }}
apiurl = "https://s.digitaloracle.co"
keychainId = str(uuid.uuid5(uuid.NAMESPACE_URL, "urn:digitaloracle.co:%s"%(mpk)))
command = "keychains"
requrl = apiurl + "/" + command + "/" + keychainId
print(requrl)
headers = {'content-type': 'application/json'}  
r = requests.post(requrl, data=json.dumps(payload), headers=headers)
r
