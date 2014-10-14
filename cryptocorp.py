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

