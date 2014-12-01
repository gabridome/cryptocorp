# take the results and build the p2sh address and script.
import json
import ast
from bitcoin.deterministic import *
from bitcoin.transaction import *
from cryptocorp import *

chainid  = "results"
if len(sys.argv) == 3:
	chainid = sys.argv[2]

path = sys.argv[1]
if len(sys.argv) <2:
	chain_file = "results"

public_keys = sub_public_keys(chainid, path)

script = mk_multisig_script(public_keys,2,3)
address = scriptaddr(script)
print("")
print("script 2 of 3:")
print(script)
print("")
print("related address: %s" % address)
print("")
