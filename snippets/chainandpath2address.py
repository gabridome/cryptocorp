# take the results and build the p2sh address and script.
import json
import ast
import bitcoin
from bitcoin.deterministic import *
from bitcoin.transaction import *

#
print(len(sys.argv))
print(sys.argv)
print(sys.argv[1])
chain_file  = "results.json"
if len(sys.argv) == 3:
	chain_file = sys.argv[2]
path = sys.argv[1]
if len(sys.argv) <1:
	chain_file = "results.json"

data = open(chain_file)
json_data = json.load(data)
json_data = ast.literal_eval(json.dumps(json_data))
private_wallets = json_data['private_wallets']
#private_wallets = ['xprv9s21ZrQH143K4XcG9k2UAQVxyDDFPcaqoum6fvjjfw8WypRy9nz1wBhFLNKponDYWsNwtgbGLqkt5uXBcW9QuAatAV5yuuGQ8aV72yiFSQw', 'xprv9s21ZrQH143K4CEt7Ds1CK4jifvPFEnUxSsJw4j6f8S8Vi9YVZhmN2dQ9nFZFdr5xKjWE7zxxz5hHABiSpdhTu9Ktw1swfgh8cqgNo76jH5']
print("")
print("Private BIP32 extended wallets")
for i in private_wallets: print(i)

print("")
public_wallets = json_data['public_wallets']
#public_wallets = [bip32_privtopub(key) for key in private_wallets]
#public_wallets.append('xpub68rQ8y4gfKNAVfmGMM8zn21nbaHw3YXnSeAktk1rcUSQ5hEjDgMSaYTQMDcBr3r2oTcpRp1P7V43HJbPpF2RzLwdxZVANWxCsVvuvfnvauh')
print("Public BIP32 extended wallets")
for i in public_wallets: print(i)

def sub_wallet(path,wallets):
	subwallets = wallets
	for i in path:
		subwallets = [bip32_ckd(key,i) for key in subwallets]
	return subwallets

# path
path = '0/0/7'
listfrompath = path.split('/')
pathinnum = [int(n) for n in (path.split('/'))] # hardened not supported


private_subwallets = sub_wallet(pathinnum,private_wallets)
print("")
print("private subwallets with path %s" % path)
for i in private_subwallets: print(i)


public_subwallets = sub_wallet(pathinnum,public_wallets)
print("")
print("public subwallets with path %s" % path)
for i in public_subwallets: print(i)

# from which the secret keys
private_keys = [bip32_extract_key(key) for key in private_subwallets]
print("")
print("private keys with path %s" % path)
for i in private_keys: print(i)

public_keys = [bip32_extract_key(key) for key in public_subwallets]
print("")
print("Public keys with path %s" % path)
for i in public_keys: print(i)

script = mk_multisig_script(public_keys,2,3)
address = scriptaddr(script)
print("")
print("script 2 of 3:")
print(script)
print("")
print("related address: %s" % address)
print("")