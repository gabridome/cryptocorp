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
import pprint
# we create two brand new BIP32 wallet (or extended keys)
# we send them to Cryptocorp with the "rules". In this case we obviously want to build a 
# 2 of 3 HDM system (Hierarchical Deterministic Multisignature)
# we obtain a third PUBLIC BIP32 Wallet (or extended keys) from which we can spend according to the "rules"
hwif1 = bip32_master_key(random_key())
hwif2 = bip32_master_key(random_key())
# estracting extended master public keys
mpk1 = bip32_privtopub(hwif1)
mpk2 = bip32_privtopub(hwif2)

print("Two extended public master keys:")
print(mpk1)
print(mpk2)
print("")

# setting the option for cryptocorp new chain. I hope to find 
# a detailed explanation in the future but for now this vlues should work
rulesetId = "default" # probably a way to save the ruleset for future use
walletAgent = "HDM-2.0-cc-022" 
keys = [mpk1, mpk2] # Our BIP32 extended public keys
asset = "BTC"
period = 60
value = 0.0
delay = 60
phone = "+123456789012" #set your telephone number
email = "name@somedomain.hot" #set here your email.

print("")
print("Options:")
print("Rule Set    : %s" % rulesetId)
print("Wallet agent: %s" % walletAgent)
print("Asset       : %s" % asset)
print("Period      : %s" % period)
print("Value       : %s" % value)
print("Delay       : %s" % delay)
print("phone       : %s" % phone)
print("Email       : %s" % email)
print("")

# preparation of the payload of the post with the options
payload =  {"rulesetId": rulesetId, "walletAgent": walletAgent, "keys": keys, "parameters": {"levels": [{"asset": asset, "period": period, "value": value}, {"delay": delay, "calls": ["phone","email"]}]},"pii": { "email": email, "phone": phone }}
apiurl = "https://s.digitaloracle.co" # sandbox URL
keychainId = str(uuid.uuid5(uuid.NAMESPACE_URL, "urn:digitaloracle.co:%s"%(mpk1)))
requrl = apiurl + "/keychains/" + keychainId
print(requrl)
# set the content type:
headers = {'content-type': 'application/json'}
pp = pprint.PrettyPrinter(indent=4)
print("the request:")
print("POST %s" % requrl)
print("Body:")
print("")
pp.pprint(payload)
print("")

# I's important to encode properly the payload. Use json.dumps(jsondata)  
r = requests.post(requrl, data=json.dumps(payload), headers=headers)
print(r.text)
mpk3 = str(r.json()['keys']['default'][0])
chainId= str(r.json()['id'])
print("")
print("My new chain ID               : %s" % chainId)
print("URL of the generated keychain : %s" % requrl)
print("Default Key                   : %s" % mpk3)
print("My public Wallet 1            : %s" % mpk1)
print("My public Wallet 2            : %s" % mpk1)
print("My private Wallet 1           : %s" % hwif1)
print("My private Wallet 2           : %s" % hwif2)
print("")
print("json string for this keychain:")
# I put Cryptocorp's public wallet as last because it requires this when you send the transaction.
json_string = {"chainid": chainId, "my_public_wallets":[mpk1,mpk2], "cryptocorp_wallet": mpk3, "private_wallets":[hwif1,hwif2], "parameters":payload['parameters'], "pii": payload['pii'], "rulesetId": payload['rulesetId'], "walletAgent": payload['walletAgent']}

pp.pprint(json_string)
with open(chainId + ".json", 'w') as outfile:
     json.dump(json_string, outfile)
print("")
print("results data written to %s.json" % chainId)
print("")