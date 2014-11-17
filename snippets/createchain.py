#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# This file is a simple example on how to create a keychain with Cryptocorp.
# Feel free to use and improve the code. 
import uuid
import binascii
import requests
import json
from pycoin.key import *
from pycoin.key.BIP32Node import BIP32Node
from pycoin.scripts.ku import * #To generate entropy

# create two random BIP32 Wallet
hwif1 = BIP32Node.from_master_secret(get_entropy())
hwif2 = BIP32Node.from_master_secret(get_entropy())


mpk1 = hwif1.hwif()
mpk2 = hwif2.hwif()

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

