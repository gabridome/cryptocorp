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
from pycoin.tx.pay_to import ScriptMultisig #per generare script e address
from pycoin.tx.pay_to import address_for_pay_to_script, build_hash160_lookup, build_p2sh_lookup #to get the address from the script
from pycoin.tx import Tx, TxIn, TxOut, SIGHASH_ALL, tx_utils
from pycoin.serialize import b2h # to print script in a readable format
from pycoin.services import blockr_io #to grab the spendables

# create two random BIP32 Wallet
hwif1 = BIP32Node.from_master_secret(get_entropy())
hwif2 = BIP32Node.from_master_secret(get_entropy())

# two new extended public keys from the newly generated node
mpk1 = hwif1.hwif()
mpk2 = hwif2.hwif()

#set the parameters for the new chain:
rulesetId = "default"
walletAgent = "HDM-2.0-cc-022"
keys = [mpk1, mpk2]
asset = "BTC"
period = 60
value = 0.0
delay = 60
phone = "+393489992529" #set your telephone number
email = "gabridome@fastmail.fm" #set here your email.

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
mpk3 = str(r.json()['keys']['default'][0])
hmpk1 = Key.from_text(mpk3)
print()
print(r.text)
# being this a demontrational code no file or directies will be created.
# I print everything for future transactions. Feel free to change the code
# for key storing inside gpg protected files etc.
print()
print("Gererated public wallet : %s" % mpk3) # created and supplied by Cryptocorp
print("BIP32 wallet n.1        : %s" % hwif1.hwif(as_private=True))
print("BIP32 wallet n.2        : %s" % hwif2.hwif(as_private=True))
print()

#path: 0/0/7 easy to remember

path = "0/0/7"


spk1 = BIP32Node.subkey_for_path(hwif1, path)
spk2 = BIP32Node.subkey_for_path(hwif2, path)
spk3 = BIP32Node.subkey_for_path(hmpk1, path)

#list of the public keys in sec format (to display them)
print("public keys in hex:")
print (BIP32Node.subkey_for_path(hwif1, path).sec_as_hex())
print (BIP32Node.subkey_for_path(hwif2, path).sec_as_hex())
print (BIP32Node.subkey_for_path(hmpk1, path).sec_as_hex())

#public subkeys in sec binary format (because ScriptMultisig requires it)
keys = [spk1, spk2, spk3] #just remember that the third has not the secret exponent
print(keys)
script = ScriptMultisig(n=2, sec_keys=[key.sec() for key in keys]).script()
print("script:")
print(b2h(script))
address = address_for_pay_to_script(script)
print(address)
# Everything's ok until here
"""
tx_in = TxIn.coinbase_tx_in(script=b'')
tx_out = TxOut(10000, script) # 0.1 mBits


tx1 = Tx(version=1, txs_in=[tx_in], txs_out=[tx_out])
"""

spendables = blockr_io.spendables_for_address(address) #grab the spendables from an address
tx = tx_utils.create_tx(spendables, [spk1.address()], fee="standard") # tx with the amount to the destination address. I take one key of which I have the secret key.
hash160_lookup = build_hash160_lookup(key.secret_exponent() for key in keys[0:2]) # only the first two are private keys

# build_hash160_lookup(key.secret_exponent() for key in keys[0:1]) # I sign only with the first one.
# also build_hash160_lookup(Key.secret_exponent(keys[0]))
tx2.sign(hash160_lookup=hash160_lookup)
tx2.as_hex() #to be tested
"""
	tx = create_tx(
        spendables_for_address("1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH"),
        [("1cMh228HTCiwS8ZsaakH8A8wze1JR5ZsP", 100)],
        fee=0)
     tx.sign_tx(wifs=["KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7rFU73sVHnoWn"])

     oppure tuuto d'un colpo:
         tx = create_signed_tx(
        spendables_for_address("1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH"),
        ["1cMh228HTCiwS8ZsaakH8A8wze1JR5ZsP"],
        wifs=["KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7rFU73sVHnoWn"],
        fee=0)

   """


