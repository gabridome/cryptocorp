#!/usr/bin/python
#Prima di tutto devo generare 128, 256 o 512 bits di entropia. Consigliati 256.
# Questo é il seed.
# Da questo con uno SHA 512 ottengo una stringa di 64 caratteri (512 bits)
# Divido la stringa in due da 128 bits (o 32 caratteri e con i primi 32 facciola Master private key e con la seconda faccio il chain code)
# Con la chiave privata ottengo una chiave pubblica.

# Con queste due e il chain code ottengo la prima coppia (pubblica e privata di extended keys (k,c) privata e (K,c) pubblica)
# Questo é il master extendeded node.
# Nella notazione ufficiale é chiamato m
# La struttura di defaul prevede che i figli siano gli accounts quindi possono essere innumerevoli.
# Ciascuno degli accounts però può avere solo due figli: 0 e 1 rispettivamente per gli indirizzi esterni e interni.
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
# Derived Public Key (in realtà é una master) 
mpk1 = "xpub661MyMwAqRbcG2ao5ER8N7AJBdLmpogJW81hes5dLXrfNF2RameUkL9GisfAt3CeqoE7oY8RdKwHKcYAZUb4MtZhnPi4ABRP185iYCrrxwT"
# Questi non verranno usati perché fanno parte di una master
msk2 = "xprv9s21ZrQH143K3TBwt5FDxr4Hse7HpxyBMiEvRa3RHKrWCqWZ9dWVfTzpirNWjYWiQQuQzYWAQsXD4PbooL3dv6wBNVEjkVH83FRFeMJCk14"
mpk2 = "xpub661MyMwAqRbcFwGQz6nEKz12RfwnERh2iwAXDxT2qfPV5dqhhApkDGKJa9hrNJXEnCjR6aXmuPrAanjeSSh6Qpo2sFCpVqDucNxon7z4un7"

msk3 = "xprv9s21ZrQH143K2wgWS7zXaxneoVibFbfpvtGRKTpWNfzv6uT8TeLR9mRaf1Heez31SwdqVg2EjK1C21JSve4iWjBkjSxoLY11GZX4nh1P4rq"
mpk3 = "xpub661MyMwAqRbcFRkyY9XXx6jPMXZ5f4PgJ7C27rE7w1XtyhnH1BefhZk4WH23KEcMxvJyote6TX5sGd1HpEvy3fB66fmhXWjFURatYZcP8sw"





#Public key (Hex) # Private key (WIF) KzpRD7AseqCJsxHGadoHwLYVPPXBBSRPcpSM9Da6Gum1Q2FmXN2m
# address 1HTTvgjWv9zdYdhCvu9biRG3gYu2RBVhCq

import pycoin
import uuid


keychainId = str(uuid.uuid5(uuid.NAMESPACE_URL, "urn:digitaloracle.co:%s"%(mpk3)))

#Ora che hai le master keys devi costruire le chiavi figlie


payload =  {
    "walletAgent": "HDM-2.0-cc-100",
    "rulesetId": "default",
    "keys": [mpk1, mpk2, mpk3],
    "parameters": {
        "levels": [ {
            "asset": "BTC",
            "period": 60,
            "value": 0.0
        }, {
            "delay": 0,
            "calls": ['phone', 'email']
        }, ]
   },
    "pii": { 
        "email": "user@example.com", 
        "phone": "+14155551212" 
    } 
}
apiurl = "https://s.digitaloracle.co"
command = "keychains"
requrl = apiurl + "/" + command + "/" + keychainId    
r = requests.post(requrl, data=payload)

