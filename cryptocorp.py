#!/usr/bin/python

#extended public keys

# preparo i New keychain parameters:
#
# Please don't forget to customize the "contacts" variable with your own references
#
#
# syntax: contacts = [{"email":"email1@somedomain.com"},{"email":"email2@somedomain.com"},{"sms":"+12345678910"},{"web":"https://somecall-back.com"}]
# The key tree

#The next step is cascading several CKD constructions to build a tree. 
# We start with one root, the master extended key m. 
# By evaluating CKDpriv(m,i) for several values of i, 
# we get a number of level-1 derived nodes. 
# As each of these is again an extended key, CKDpriv can be applied to those as well.

#To shorten notation, we will write CKDpriv(CKDpriv(CKDpriv(m,3H),2),5) as m/3H/2/5. Equivalently for public keys, we write CKDpub(CKDpub(CKDpub(M,3),2,5) as M/3/2/5. This results in the following identities:

#N(m/a/b/c) = N(m/a/b)/c = N(m/a)/b/c = N(m)/a/b/c = M/a/b/c.
#N(m/aH/b/c) = N(m/aH/b)/c = N(m/aH)/b/c.
#However, N(m/aH) cannot be rewritten as N(m)/aH, as the latter is not possible.
#Each leaf node in the tree corresponds to an actual key, while the internal nodes correspond to the collections of keys that descend from them. The chain codes of the leaf nodes are ignored, and only their embedded private or public key is relevant. Because of this construction, knowing an extended private key allows reconstruction of all descendant private keys and public keys, and knowing an extended public keys allows reconstruction of all descendant non-hardened public keys.

#  m = Master extended key (Pieter Wuille)

############################ uno
# bip32 extended  key = m = the "seed" = master extended key
bip32xk = "xprv9s21ZrQH143K3YWKyCt7zyDZdbWHRLxT8u66rUg1nCKgVShH3ELECXpnsaCgSMfRv3GpxT4cLH8Xy1YvPqYJDF2QagYya8oa7Hb7YQgyZgN"
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
dpk = "xpub661MyMwAqRbcG2ao5ER8N7AJBdLmpogJW81hes5dLXrfNF2RameUkL9GisfAt3CeqoE7oY8RdKwHKcYAZUb4MtZhnPi4ABRP185iYCrrxwT"
# Questi non verranno usati perché fanno parte di una master

#Public key (Hex) # Private key (WIF) KzpRD7AseqCJsxHGadoHwLYVPPXBBSRPcpSM9Da6Gum1Q2FmXN2m
# address 1HTTvgjWv9zdYdhCvu9biRG3gYu2RBVhCq


keychainId = str(uuid.uuid5(uuid.NAMESPACE_URL, "urn:digitaloracle.co:%s"%(dpk)))

#Ora che hai le master keys devi costruire le chiavi figlie

payload =  {
    "walletAgent": "HDM-2.0-cc-100",
    "rulesetId": "default",
    "keys": [ epk1,epk2,epk3 ],
    "parameters": {
        "velocity_1": {
            "value": 0.8,
            "asset": "BTC",
            "period": "86400",
            "limited_keys": ["3"]
        },
        "delay_2": 600,
        "call_2": ["phone"], 
        "verify_2": ["otp"],
        "otp_type": "totp",
        "otp_secret": "IS3TZZIPTDPM2YGT4CDXEOFK",
        "otp": "123456"
    },
   "pii": {
        "email": "gabridome@fastmail.fm",
        "phone": "+393489992529",
    }
}
apiurl = "http://s.digitaloracle.co/"
command = "keychains"
requrl = apiurl + "/" + command + "/" + keychainId    
r = requests.post(requrl, data=payload)

