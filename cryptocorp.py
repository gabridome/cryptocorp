#!/usr/bin/python

#extended public keys

epk1 = "xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8"
epk2 = "xpub661MyMwAqRbcFW31YEwpkMuc5THy2PSt5bDMsktWQcFF8syAmRUapSCGu8ED9W6oDMSgv6Zz8idoc4a6mr8BDzTJY47LJhkJ8UB7WEGuduB"
epk3 = "xpub661MyMwAqRbcFW31YEwpkMuc5THy2PSt5bDMsktWQcFF8syAmRUapSCGu8ED9W6oDMSgv6Zz8idoc4a6mr8BDzTJY47LJhkJ8UB7WEGuduB"
keychainId = str(uuid.uuid5(uuid.NAMESPACE_URL, "urn:digitaloracle.co:%s"%(epk1)))
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

# preparo i New keychain parameters:
#
# Please don't forget to customize the "contacts" variable with your own references
#
#
# syntax: contacts = [{"email":"email1@somedomain.com"},{"email":"email2@somedomain.com"},{"sms":"+12345678910"},{"web":"https://somecall-back.com"}]

############################ uno
#bip32 extended  key
bip32xk = "xprv9s21ZrQH143K3YWKyCt7zyDZdbWHRLxT8u66rUg1nCKgVShH3ELECXpnsaCgSMfRv3GpxT4cLH8Xy1YvPqYJDF2QagYya8oa7Hb7YQgyZgN"
# Bitcoin Master Private Key
# Version 0488ade4
# Depth 0
# Parent Fingerprint 00000000
# Child Index 0
# Chain Code 95306ebe1fca3fe7ad0060e721697a8cc62df1ffb02dc5ea4552dca8e5334087
# Key KzpRD7AseqCJsxHGadoHwLYVPPXBBSRPcpSM9Da6Gum1Q2FmXN2m
#derivation path m/k'/0
#Account 0
# Derived private key xprv9xMnJ1qUk7GvB9vhDNNxLFvWXZd8xc2Ybz13poJAP4wUL4gdYQx22YkbsmjPHcaHP7Q3LLtBug56g8GXKgmogWkc4zW4hzsm7MbNUqEVeYE
# Private Key (WIF) KyUGzsjcy6t1h4DaSFY4SDRoozkHmGyhvAg7kudShpXAFATAGRYQ
# Derived Public Key 
dpk1 = xpub6BM8hXNNaUqDPe1AKPuxhPsF5bTdN4kPyCvedBhmwQUTCs1n5xGGaM55j5TT8UJtNu4BaSFPTFTPGzUo27TETZJbLxpzYzVcSxo2Rdpp3TX
# private key 03a610f61a2427aecdd43c8162de4df2c0959c58c166a7f53d5c16139ab04e96aa
# Address 14P6msMsAnFLmCMFaU6WVbm1XsRgb1EVaR

############################ due
#bip32 extended  key
bip32xk = "xprv9s21ZrQH143K2Lvmu2jegpB2Bc6QjGxXnJyNZ7EGY19x2iwT6KvqYm3K3JunsFH2YxdpQFAwnysoBemmRm1XyLambgP4Pi3hcJE7Lek2QTK"
# Bitcoin Master Private Key
# Version 0488ade4
# Depth 0
# Parent Fingerprint 00000000
# Child Index 0
# Chain Code 1cb24ba9c92d3673ba0dd1fed2a28fc8d08b03a7ae89fde4be598da18e9a4434
# Key KzzZrbpuzkQ7SQ8RRX2yDbFKPLrWX2WA8oMnkDamqpkYS12MoXZj
#derivation path m/k'/0
#Account 0
# Derived private key xprv9w5h9Gd6tRXYfsYYGuYKnucjhTLZfNHB1pkxdcm4xvTAVWaAVakqvGnCqBKMFJyQ25PdjTdFTBt7wYJZfSYPNvxVEBuxyZ9mye9ZemiNJJF
# Private Key (WIF) L1XsuXkT5Sr9Pqq31srFz12QGCjsin2b9YjiDdbupRvkJ6dzMynU
# Derived Public Key 
dpk2 ="xpub6A53Yn9zio5qtMd1Nw5LA3ZUFVB44q12P3gZS1AgXFz9NJuK3856U56ggV2JCAWSQJBvES5XrPQR4sysWBaVUGwQt1EmBVMeihPNTYeJK8P"
# public key 03e10da963e4b5f5807dcf215607125f945919fb6ded2196f573c3e514284df676
# Address 1MauEtN3FNYFpnBvuZJjd7GB8DKcfRtYq4

############################ tre
#bip32 extended  key
bip32xk = "xprv9s21ZrQH143K38TsTdRrSofjBLLp9nGjfT6sMzP8GibT9263LkwNXh5rQkbfH7TJorkLgDBEPd5kGb5KLhQ9oQT6wBAod8ZGuUPz4BeeL1u"
# Bitcoin Master Private Key
# Version 0488ade4
# Depth 0
# Parent Fingerprint 00000000
# Child Index 0
# Chain Code 6b8dc4149b973c8a1297fd661ffabcde962eb4fbf4f4685e9644cd197007841e
# Key KzzZrbpuzkQ7SQ8RRX2yDbFKPLrWX2WA8oMnkDamqpkYS12MoXZj
#derivation path m/k'/0
#Account 0
# Derived private key xprv9wSA1cCLEDiwyLfDt87hUfLkwvzg9TvLYW62H4CPDJSWwxe3gy61sLtegPgTAxBWH7wwxDgqVsnuPQ9X6ahVVGfR2nEUGbFK37j91M5kr54
# Private Key (WIF) L4DDsieEt3HU9m6wEahDXwxGhkn4HYpEb5NJg4cBJnxmNxGoFLV2
# Derived Public Key 
dpk3 = "xpub6ARWR7jE4bHFBpjgz9ehqoHVVxqAYveBuj1d5SbzmdyVpkyCEWQGR9D8XdXMksnhSM6TMN55sB3YazwysaFcbgUv3vJVoqSMgVE6bFr2UGP"
# public key 03e10da963e4b5f5807dcf215607125f945919fb6ded2196f573c3e514284df676
# Address 1MauEtN3FNYFpnBvuZJjd7GB8DKcfRtYq4


