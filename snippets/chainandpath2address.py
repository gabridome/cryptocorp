# take the results and build the p2sh address and script.
import json
import ast
from bitcoin.deterministic import *
from bitcoin.transaction import *
from cryptocorp import *

chainid  = "pythonresults"
if len(sys.argv) == 3:
	chainid = sys.argv[2]

path = sys.argv[1]
if len(sys.argv) <3:
	chain_file = "results"

path = "0/0/7"

data = json.load(open((chain_file + ".json"), "r"))
public_wallets = data['keys']
public_wallets.extend(data['cryptocorp_MPEK'])

public_sub_wallets = [sub_wallet(path,wallet) for wallet in public_wallets] 

public_keys = [bip32_extract_key(wallet) for wallet in public_sub_wallets]

script = mk_multisig_script(public_keys,2,3)
address = scriptaddr(script)
print("")
print("script 2 of 3:")
print(script)
print("")
print("related address: %s" % address)
print("")
