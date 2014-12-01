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


mk_multisig_script(sub_public_keys(chainid, path),2,3)
script = mk_multisig_script(sub_public_keys(chainid, path),2,3)
address = scriptaddr(script)
print("")
print("script 2 of 3:")
print(script)
print("")
print("related address: %s" % address)
print("")
