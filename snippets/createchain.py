#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# This file is a simple example on how to create a keychain with Cryptocorp.
# Feel free to use and improve the code. 
import uuid
import binascii
import requests
import json
from pycoin.key import *

#http://ms-brainwallet.org/#bip32 is a site where you can generate a bunch of keys for testing
# 
# You must provide two BIP32 Extended keys. Here below are the "xprv...." strings. Substitute those with yours.

# Extended Private key number 1:
bip32w1 = Key.from_text("xprv9s21ZrQH143K2rQnHxHvkQ2N5EQNy8JN76hnJSm8TYfLNBeJb9f94D79LWBjwscqfeykyvHMeufJALHyy4iqPSd81rgft3777U36eKsYgSA")

# Extended Private key number 2:

bip32w2 = Key.from_text("xprv9s21ZrQH143K3meYuDjr6RAzhYdZLj8KMJvkbsZhhLfgC7TL5iMREmoGnStr255EQqf4cgCSoM3r9SDxWNpEk62D8RgwHWqQSSteyDZfSKf")

# Obtaining the  public extended bip32 keys

mpk1 = bip32w1.hwif()
mpk2 = bip32w2.hwif()

#set the parameters for the new chain:
rulesetId = "default"
walletAgent = "HDM-2.0-cc-011"
keys = [mpk1, mpk2]
asset = "BTC"
period = 60
value = 0.0
delay = 60
phone = "+123456789012"
email = "youremailuser@youremaildomain.com"

payload =  {"rulesetId": rulesetId, "walletAgent": walletAgent, "keys": keys, "parameters": {"levels": [{"asset": asset, "period": period, "value": value}, {"delay": delay, "calls": ["phone","email"]}]},"pii": { "email": email, "phone": phone }}
apiurl = "https://s.digitaloracle.co"
keychainId = str(uuid.uuid5(uuid.NAMESPACE_URL, "urn:digitaloracle.co:%s"%(mpk1)))
command = "keychains"
requrl = apiurl + "/" + command + "/" + keychainId
print(requrl)
# set the content type:
headers = {'content-type': 'application/json'}
# I's important to encode properly the payload. Use json.dumps(jsondata)  
r = requests.post(requrl, data=json.dumps(payload), headers=headers)
r.json()

