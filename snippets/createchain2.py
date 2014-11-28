#!/usr/bin/python
# this version utilize pybitcointools to deal with transactions.
import sys
import uuid
import requests
import bitcoin
import time
import os
from bitcoin.deterministic import *
from bitcoin.transaction import *
from bitcoin.bci import *

# we create two brand new BIP32 wallet
hwif1 = bip32_master_key(random_key())
hwif2 = bip32_master_key(random_key())
# estracting extended master public keys
mpk1 = bip32_privtopub(hwif1)
mpk2 = bip32_privtopub(hwif2)

print("Two extended public master keys:")
print(mpk1)
print(mpk2)
print()

#setting the option for cryptocorp new chain
rulesetId = "default"
walletAgent = "HDM-2.0-cc-022"
keys = [mpk1, mpk2]
asset = "BTC"
period = 60
value = 0.0
delay = 60
phone = "+123456789012" #set your telephone number
email = "name@somedomain.hot" #set here your email.

print()
print("Options:")
print("Rule Set    : %s" % rulesetId)
print("Wallet agent: %s" % walletAgent)
print("Asset       : %s" % asset)
print("Period      : %s" % period)
print("Value       : %s" % value)
print("Delay       : %s" % delay)
print("phone       : %s" % phone)
print("Email       : %s" % email)
print()

# preparation of the payload of the post with the options
keychainId = str(uuid.uuid5(uuid.NAMESPACE_URL, "urn:digitaloracle.co:%s" % (mpk1)))
payload =  {"rulesetId": rulesetId, "walletAgent": walletAgent, "keys": keys, "parameters": {"levels": [{"asset": asset, "period": period, "value": value}, {"delay": delay, "calls": ["phone","email"]}]},"pii": { "email": email, "phone": phone }}
apiurl = "https://s.digitaloracle.co" # sandbox URL
keychainId = str(uuid.uuid5(uuid.NAMESPACE_URL, "urn:digitaloracle.co:%s" % (mpk1)))
command = "keychains"
requrl = apiurl + "/" + command + "/" + keychainId

# set the content type:
headers = {'content-type': 'application/json'}
# I's important to encode properly the payload. Use json.dumps(jsondata)  
r = requests.post(requrl, data=json.dumps(payload), headers=headers)
r.json()
mpk3 = str(r.json()['keys']['default'][0])
chainId= str(r.json()['id'])
print()
print(r.text)
print("My new chain ID               : %s" % chainId)
print("URL of the generated keychain : %s" % requrl)
print("Default Key                   : %s" % mpk3)
print("My public Wallet 1            : %s" % mpk1)
print("My public Wallet 2            : %s" % mpk1)
print("My private Wallet 1           : %s" % hwif1)
print("My private Wallet 2           : %s" % hwif2)
print()
print("json string for this keychain:")
json_string = {"chainid": chainId, "public_wallets":[mpk3,mpk1,mpk2], "private_wallets":[hwif1,hwif2], "payload": payload}
print(json.dumps(json_string))
with open('results.json', 'w') as outfile:
     json.dump(json_string, outfile)
print("results data written to results.json")
