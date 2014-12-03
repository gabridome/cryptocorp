# take the results and build the p2sh address and script.
import json
import ast
from bitcoin.deterministic import *
from bitcoin.transaction import *
from cryptocorp import *

chainid  = "pythonresults"

chain_file = "results"

path = "0/0/7"

result_script = "5221033cb2f8b318f4c14e42cbe20cb365b2017d28bc557b0dde9eca2fbe8d3c9ed1982102e680e729a24923c09db6f958363b0416bc13970008ab7b925b2f2aa410e6b0a72102208fa0a00d6b9ae56f7cc137a021d03ae294d39242d64322f69bdc785853ba6453ae"
result_address = "3Bi36w9RZHmibi1ip7ud9dvtpDt59ij7GC"

data = json.load(open((chain_file + ".json"), "r"))
public_wallets = data['keys']
public_wallets.extend(data['cryptocorp_MPEK'])

public_sub_wallets = [sub_wallet(path,wallet) for wallet in public_wallets] 

public_keys = [bip32_extract_key(wallet) for wallet in public_sub_wallets]

script = mk_multisig_script(public_keys,2,3)
address = scriptaddr(script)

if address == result_address: print("success!!")
if script == result_script: print("success!!")

print("")
