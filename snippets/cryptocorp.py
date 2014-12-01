#!/usr/bin/python
# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding: utf-8 -*-
# This is the library for the common functions necessary with cryptocorp.co/api
# You can create a new chain and/or use the new chain to make transactions using 
# a particular subkey agreeing with cryptocorp on the path.
from bitcoin.deterministic import *
from bitcoin.transaction import *
import ast
import requests
import uuid
import json
# The most important thing we have to provide are the Master Public Extended Keys.
# If we provide One MPEK we will have a 2of2 HDM structure: both private keys (our and Cryptocorp's)
# will be necessary to spend the funds.
# If we provide two MPEK we will have a 2of3 HDM structure. We will be able to store one secret key in a safe
# and to use it a) if we loose the other key b) if we want to redeem the funds without Cryptocorp approving
# (Zero Trust structure).
# You should use your own key but in case you need a pair:
# mseks = [bip32_master_key(random_key()) for i in range(2)]
# mpeks = [bip32_privtopub(i) for i in mseks]


def createchain(mpeks,rulesetId="default",walletAgent="HDM-2.0-cc-011",asset="BTC",period=60,value=0.0,delay = 60,phone="+123456789012",email="name@somedomain.on"
):
    payload =  {"rulesetId": rulesetId, "walletAgent": walletAgent, "keys": mpeks, "parameters": {"levels": [{"asset": asset, "period": period, "value": value}, {"delay": delay, "calls": ["phone","email"]}]},"pii": { "email": email, "phone": phone}}
    apiurl = "https://s.digitaloracle.co"
    keychainId = str(uuid.uuid5(uuid.NAMESPACE_URL, "urn:digitaloracle.co:%s" % (mpeks)))
    command = "keychains"
    requrl = apiurl + "/" + command + "/" + keychainId
    print(requrl)
    headers = {'content-type': 'application/json'}  
    r = requests.post(requrl, data=json.dumps(payload), headers=headers)
    if "error" in (r.text): return (r.text)
    cryptocorp_MPEK = r.json()['keys']['default']
    chain_json = {"rulesetId": rulesetId, "walletAgent": walletAgent, "keys": mpeks, "cryptocorp_MPEK": cryptocorp_MPEK, "keychainId": keychainId, "parameters": {"levels": [{"asset": asset, "period": period, "value": value}, {"delay": delay, "calls": ["phone","email"]}]},"pii": { "email": email, "phone": phone }}
    return chain_json

# the indexes with "'" are transformed in 2**31 + i and everything is converted in int()

def pathInt(path):
    listfrompath = path.split('/')
    pathinnum = []
    for f in listfrompath:
        if "'"  in f: pathinnum.append(2**31+int(f[:-1]))  
        else: pathinnum.append(int(f))
    return pathinnum

def sub_wallets(path,wallets):
    pathinnum = pathInt(path)
    subwallets = wallets
    for i in pathinnum:
        subwallets = [bip32_ckd(key,i) for key in subwallets]
    return subwallets

def sub_public_keys(chainid, path, ext=".json"):
    chain_file = chainid + ext
    json_data = json.load(open(chain_file))
    json_data = ast.literal_eval(json.dumps(json_data))
    mpkes = json_data['keys']
    mpkes.append(json_data['cryptocorp_MPEK'][0])
    subwallets = sub_wallets(path,mpkes)
    public_keys = [bip32_extract_key(key) for key in subwallets]
    return public_keys


