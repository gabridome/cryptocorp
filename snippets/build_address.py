# take the results and build the p2sh address and script.
import json
import ast
import bitcoin
from bitcoin.deterministic import *


# Scrive un file.
data = open("results.json")
json_data = json.load(data)
json_data = ast.literal_eval(json.dumps(json_data))
private_wallets = json_data['private_wallets']
public_wallets = json_data['public_wallets']
#costruisco un figlio
publics = [bip32_ckd(key,5) for key in public_wallets] #it works
privates = [bip32_ckd(key,5) for key in private_wallets]

# path
path = '0/0/7'
listfrompath = path.split('/')
pathinnum = [int(n) for n in (path.split('/'))]

# from which the public keys
public_keys = [bip32_extract_key(key) for key in publics]
private_keys = [bip32_extract_key(key) for key in privates]

script = mk_multisig_script(public_keys,2,3)
address = scriptaddr(script)