from cryptocorp import *
import pprint
pp = pprint.PrettyPrinter(indent=4)
# creating wallets
mseks = [bip32_master_key(random_key()) for i in range(2)]
# creating public wallets
mpeks = [bip32_privtopub(i) for i in mseks]

# you can personalize as follows:
# rulesetId = "default" # probably a way to save the ruleset for future use
# walletAgent = "HDM-2.0-cc-021" 
# asset = "BTC"
# period = 60
# value = 0.0
# delay = 60
# phone = "+123456789012" #set your telephone number
# email = "name@somedomain.hot" #set here your email.
# obviously if you want to use your own existent BIP32 Master Public Keys
# you will put them in mpeks list instead of generating two brand new.

new_chain_json = createchain(mpeks)
print("")
pp.pprint(new_chain_json)
print("")
with open(new_chain_json['keychainId'] + ".json", 'w') as outfile:
     json.dump(new_chain_json, outfile)

with open(new_chain_json['keychainId'] + ".mseks.json", 'w') as outfile:
     json.dump(mseks, outfile)

print("")
print("results data written to %s.json" % new_chain_json['keychainId'])
print("")
