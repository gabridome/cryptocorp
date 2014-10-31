#!/usr/bin/python
from pycoin.key import *
from pycoin.key.BIP32Node import *
from pycoin.serialize import b2h
import uuid
import binascii

# Prima di tutto devo generare 128, 256 o 512 bits di entropia. Consigliati 256.
# Questo e' il seed.
# Da questo con uno SHA 512 ottengo una stringa di 64 caratteri (512 bits)
# Divido la stringa in due da 128 bits (o 32 caratteri e con i primi 32 facciola Master private key e con la seconda faccio il chain code)
# Con la chiave privata ottengo una chiave pubblica.

# Con queste due e il chain code ottengo la prima coppia (pubblica e privata di extended keys (k,c) privata e (K,c) pubblica)
# Questo e' il master extendeded node.
# Nella notazione ufficiale e' chiamato m
# La struttura di defaul prevede che i figli siano gli accounts quindi possono essere innumerevoli.
# Ciascuno degli accounts pero' puo' avere solo due figli: 0 e 1 rispettivamente per gli indirizzi esterni e interni.
# I figli esterni ed interni possono poi avere innumerevoli figli e nipoti. Es: primo account (0), esterno (0) portafoglio 532 =m/0/0/532


#To shorten notation, we will write CKDpriv(CKDpriv(CKDpriv(m,3H),2),5) as m/3H/2/5. Equivalently for public keys, we write CKDpub(CKDp
# Master key generation

# Generate a ********* seed *********** byte sequence S of a chosen length (between 128 and 512 bits; 256 bits is advised) from a (P)RNG.
# Calculate I = HMAC-SHA512(Key = "Bitcoin seed", Data = S)
# Split I into two 32-byte sequences, IL and IR.
# Use parse256(IL) as master secret key, and IR as master chain code.


############################ uno
# bip32 extended  key = m = master extended key
msk1 = "xprv9s21ZrQH143K3YWKyCt7zyDZdbWHRLxT8u66rUg1nCKgVShH3ELECXpnsaCgSMfRv3GpxT4cLH8Xy1YvPqYJDF2QagYya8oa7Hb7YQgyZgN"
# Bitcoin Master Private Key
# Version 0488ade4
# Depth 0
# Parent Fingerprint 00000000
# Child Index 0
# Chain Code 95306ebe1fca3fe7ad0060e721697a8cc62df1ffb02dc5ea4552dca8e5334087
# Key KzpRD7AseqCJsxHGadoHwLYVPPXBBSRPcpSM9Da6Gum1Q2FmXN2m


# impostando a "m" per master si ottiene
# Private key (WIF) KzpRD7AseqCJsxHGadoHwLYVPPXBBSRPcpSM9Da6Gum1Q2FmXN2m
# Derived Public Key (in realta' e' una master) 
mpk1 = "xpub661MyMwAqRbcG2ao5ER8N7AJBdLmpogJW81hes5dLXrfNF2RameUkL9GisfAt3CeqoE7oY8RdKwHKcYAZUb4MtZhnPi4ABRP185iYCrrxwT"
# Questi non verranno usati perche' fanno parte di una master

msk2 = "xprv9s21ZrQH143K3TBwt5FDxr4Hse7HpxyBMiEvRa3RHKrWCqWZ9dWVfTzpirNWjYWiQQuQzYWAQsXD4PbooL3dv6wBNVEjkVH83FRFeMJCk14"
mpk2 = "xpub661MyMwAqRbcFwGQz6nEKz12RfwnERh2iwAXDxT2qfPV5dqhhApkDGKJa9hrNJXEnCjR6aXmuPrAanjeSSh6Qpo2sFCpVqDucNxon7z4un7"

msk3 = "xprv9s21ZrQH143K2wgWS7zXaxneoVibFbfpvtGRKTpWNfzv6uT8TeLR9mRaf1Heez31SwdqVg2EjK1C21JSve4iWjBkjSxoLY11GZX4nh1P4rq"
mpk3 = "xpub661MyMwAqRbcFRkyY9XXx6jPMXZ5f4PgJ7C27rE7w1XtyhnH1BefhZk4WH23KEcMxvJyote6TX5sGd1HpEvy3fB66fmhXWjFURatYZcP8sw"





#Public key (Hex) # Private key (WIF) KzpRD7AseqCJsxHGadoHwLYVPPXBBSRPcpSM9Da6Gum1Q2FmXN2m
# address 1HTTvgjWv9zdYdhCvu9biRG3gYu2RBVhCq


keychainId = str(uuid.uuid5(uuid.NAMESPACE_URL, "urn:digitaloracle.co:%s"%(mpk3)))

#Ora che hai le master keys devi costruire le chiavi figlie
# Per generare delle chiavi master bip32 extended puoi partire da una frase:
# BIP32Node.from_master_secret("Questa frase molto lunga deve essere con abbastanza entropiahwxuwhm984")
# Oppure genero un portafoglio da una BIP32 extended master key. Es dal test vector numero 1
# BIP32Node.from_hwif("xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi")

mypriv = BIP32Node.from_hwif(msk1)
#
# I build a wallet frm vector 1
testvector1 = BIP32Node.from_hwif("xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi")
#########
print()
print ("Now BIP32Node:")
print()
print("Master secret key               : " + testvector1.hwif(as_private=True))
print("Extended Master Public key      : " + testvector1.hwif())
print("Chain code                      : " + b2h(testvector1.chain_code()))
print()
print("Key fingerprint                 : " + b2h(testvector1.fingerprint()))
print("Key depth                       : " + str(testvector1.tree_depth()))
print("Child index                     : " + str(testvector1.child_index()))
print("WIF format master key (unuseful): " + str(Key.wif(testvector1)))
print("Textual representation of key   : " + str(Key.as_text(testvector1)))
print("public pair of the key          : " + str(Key.public_pair(testvector1)))
print("Master key in hex format        : " + str(Key.sec_as_hex(testvector1)))
print("Address of the key              : " + str(Key.address(testvector1,use_uncompressed=False)))
print()
print()
print("Subkey:")
path = "0H/1/2H/2/1000000000"
mynewsubkey = BIP32Node.subkey_for_path(testvector1, path)
print("the path is                     : " + path)
print("new key depth                   : " + str(mynewsubkey.tree_depth()))
print("Child index                     : " + str(mynewsubkey.child_index()))
print("subkey extended public          : " + mynewsubkey.hwif())
print("subkey extended private         : " + mynewsubkey.hwif(as_private=True))
print("Key fingerprint                 : " + b2h(mynewsubkey.fingerprint()))
print("Secret exponent                 : " + str(mynewsubkey.secret_exponent()))
print("The key for the p2sh:")
print("WIF key                         : " + mynewsubkey.wif())
print("Public key to use in multisig   : " + Key.sec_as_hex(mynewsubkey))
print("Address                         : " + mynewsubkey.address())
print()
print()
print()

rulesetId = "default"
walletAgent = "HDM-2.0-cc-011"
keys = [mpk1, mpk2]
asset = "BTC"
period = 60
value = 0.0
delay = 60
phone = "+393489992529"
email = "gabridome@fastmail.fm"

def createchain(email,phone,mpk):
    payload =  {"rulesetId": rulesetId, "walletAgent": walletAgent, "keys": keys, "parameters": {"levels": [{"asset": asset, "period": period, "value": value}, {"delay": delay, "calls": ["phone","email"]}]},"pii": { "email": email, "phone": phone }}
    apiurl = "https://s.digitaloracle.co"
    keychainId = str(uuid.uuid5(uuid.NAMESPACE_URL, "urn:digitaloracle.co:%s"%(mpk)))
    command = "keychains"
    requrl = apiurl + "/" + command + "/" + keychainId
    print(requrl)
    headers = {'content-type': 'application/json'}  
    r = requests.post(requrl, data=json.dumps(payload), headers=headers)
    return r


def verify(email, phone, mpk):
    payload =  {"walletAgent": "HDM-2.0-cc-test",
    "pii": { 
    "email": email, 
    "phone": phone } ,
    "call": "phone"}
    keychainId = str(uuid.uuid5(uuid.NAMESPACE_URL, "urn:digitaloracle.co:%s"%(mpk3)))
    apiurl = "https://s.digitaloracle.co"
    command = "verifypii"
    requrl = apiurl + "/keychains/" + keychainId + "/" + command
    print(requrl)
    headers = {'content-type': 'application/json'}  
    r = requests.post(requrl, data=json.dumps(payload), headers=headers)
    return r
