# take the results and build the p2sh address and script.
# syntax: chainn
import json
import ast
from bitcoin.deterministic import *
from bitcoin.transaction import *
from cryptocorp import *

if len(sys.argv) == 3:
    chainid = sys.argv[2]
    path = sys.argv[1]
else:
    chainid = "a9fb11d4-ccfb-5636-8a62-063a89f34874"
    path = "0/0/7"

print("")
print("path: %s" % path)
print("")
print("chainid: %s" % chainid)
#path of the chains:
chains_path = '../chains'
os.chdir(chains_path)
data = json.load(open((chainid + "/chain.json"), "r"))
public_wallets = data['keys']
public_wallets.extend(data['cryptocorp_MPEK'])

public_sub_wallets = [sub_wallet(path,wallet) for wallet in public_wallets] 

public_keys = [bip32_extract_key(wallet) for wallet in public_sub_wallets]

script = mk_multisig_script(public_keys,2,3)
address = scriptaddr(script)
print("")
print("nodi pubblici:")
print("1: %s" % public_wallets[1])
print("")
print("2: %s" % public_wallets[2])
print("")
print("cryptocorp\'s wallet: %s" % public_wallets[1])
print("")
print("script 2 of 3:")
print(script)
print("")
print("related address: %s" % address)
print("")
