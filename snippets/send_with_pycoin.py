
# -*- coding: utf-8 -*-
import os
import json
import pprint
from pycoin.key.BIP32Node import BIP32Node
from pycoin.key import Key
from pycoin.tx.pay_to import ScriptMultisig, address_for_pay_to_script, build_hash160_lookup, build_p2sh_lookup
from pycoin.serialize import b2h

from pycoin.services import spendables_for_address
from pycoin.tx.tx_utils import create_tx
# this version uses pycoin lib.
# the first part just to verify that I can produce address and script

chains_path = '../chains'
os.chdir(chains_path)
chainid  = "a9fb11d4-ccfb-5636-8a62-063a89f34874"
result_address = '3Bi36w9RZHmibi1ip7ud9dvtpDt59ij7GC'
result_script = '5221033cb2f8b318f4c14e42cbe20cb365b2017d28bc557b0dde9eca2fbe8d3c9ed1982102e680e729a24923c09db6f958363b0416bc13970008ab7b925b2f2aa410e6b0a72102208fa0a00d6b9ae56f7cc137a021d03ae294d39242d64322f69bdc785853ba6453ae'
data = json.load(open((chainid + "/chain.json"), "r"))
print("Chain:")
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(data)
print("")

private_wallets = json.load(open((chainid + "/chain.mseks.json"), "r"))

print("Private wallets:")
pp.pprint(private_wallets)
print("")

#private_wallets.remove(private_wallets[1])
#print("Single Private wallets:")
#pp.pprint(private_wallets)
#print("")

# You have to provide YOUR masterkeys to the service for authentication
masterKeys = data['keys'] 
public_wallets = masterKeys 
public_wallets.extend(data['cryptocorp_MPEK'])

# Also cryptocorp's key is supplyed
chainPaths = ["0/0/7","0/0/7","0/0/7"]
print("Chain paths:")
pp.pprint(chainPaths)
print("")

# masterbip32nodes = [Key.from_text(i) for i in public_wallets]

sub_bip32_nodes = [BIP32Node.subkey_for_path(Key.from_text(public_wallets[i]), chainPaths[i]) for i in range(len(chainPaths))]
print("Sub BIP32 wallets:")
for i in sub_bip32_nodes:
    print(i)

print("")

script_encoded = ScriptMultisig(n=2, sec_keys=[key.sec() for key in sub_bip32_nodes]).script()

script = b2h(script_encoded)
print("Script:")
print(script)
print("")

address = address_for_pay_to_script(script_encoded)
# 3Bi36w9RZHmibi1ip7ud9dvtpDt59ij7GC

print("Address: %s" % address)
print("")

spendables = spendables_for_address(address)
# UTXOs of address

# The simplest transaction: all the UTXOs, less the fees, go to the address.
tx = create_tx(spendables,["3977Lp7VNWY5L8hY5W2oaNjeR5r8FZ6ban"], fee="standard")
# raw hex not-signed transaction

tx.as_hex()
# to sign the transaction I need the sub_private keys
print("Transaction as Hex:")
print(tx.as_hex(tx))
print("")

# My Extended private subkeys
subBip32PrivateNodes = [BIP32Node.subkey_for_path(Key.from_text(private_wallets[i]), chainPaths[i]) for i in range(len(private_wallets))] # subnodes

print("Sub BIP32 private wallets:")
for i in subBip32PrivateNodes:
    print(i)

print("")

"""
# beginning part totally signed
hash160_lookup = build_hash160_lookup([subBip32PrivateNodes[i].secret_exponent() for i in range(len(subBip32PrivateNodes))])
# >>> [subBip32PrivateNodes[i].secret_exponent() for i in range(len(subBip32PrivateNodes))]
# [110380562092968897127842430006032843930864261596730345665503170493711194530512, 73231854494958203118397405284330291107828238186602400029170683163884922382627]
p2sh_lookup = build_p2sh_lookup([script_encoded])
p2sh_lookup = build_p2sh_lookup([script_encoded])
tx.sign(hash160_lookup=hash160_lookup, p2sh_lookup=p2sh_lookup)
tx.bad_signature_count() # checking if the signature process has worked
tx.as_hex() # is the raw hex correctly signed transaction
# 01000000020076ae0b7d8b4b7b44ac0b2fe2d5dc67aabbf0898291f190c7f9004f3923744301000000fc0047304402206fa07cce3d3c76dfb837c06bea796cb5b15e9075be6f20c708175662b3439c840220110fdc96c589ccaaf019e0678efd9aa2770661fb9f61227fb34b283a433b29110147304402207fb7f368d9458dd4d5afdf2ba89f42e5420634418759cdc8438f6ece60494b9d02203efe6428ec53bd08665300470f5e21f80f37fdb131281810f3b539d8268371e7014c695221033cb2f8b318f4c14e42cbe20cb365b2017d28bc557b0dde9eca2fbe8d3c9ed1982102e680e729a24923c09db6f958363b0416bc13970008ab7b925b2f2aa410e6b0a72102208fa0a00d6b9ae56f7cc137a021d03ae294d39242d64322f69bdc785853ba6453aeffffffffbbedb48aacb4dcea45687631cf592035843e754f603f7615b590d2b2f12e858d00000000fdfe0000483045022100f3a6e2cac3ffd51c85bfa0162d60ab125d669bb31b735563b8b4f47cf9fd7495022019f9a668d4c984e1da7f9ff16321bed57df66f7a80a953cc798682204b91e4f301483045022100c6d9226dccee03fcd9539db6780e0c9af1e096b260e4b60852c4ba1c2d1c9810022061bfa26cb8984aac054d6525cb7aeb9ce2d77021233e15928c2668de60848704014c695221033cb2f8b318f4c14e42cbe20cb365b2017d28bc557b0dde9eca2fbe8d3c9ed1982102e680e729a24923c09db6f958363b0416bc13970008ab7b925b2f2aa410e6b0a72102208fa0a00d6b9ae56f7cc137a021d03ae294d39242d64322f69bdc785853ba6453aeffffffff01803801000000000017a914b2f5e0dfcfa103a0fb4208c3393c30ff3204b5d78700000000

# end part totally signed
"""
# To sign the transaction for cryptocorp I will sign with just one of the two private keys required let's choose the first.

hash160_lookup = build_hash160_lookup([subBip32PrivateNodes[0].secret_exponent()])
p2sh_lookup = build_p2sh_lookup([script_encoded])
tx2.sign(hash160_lookup=hash160_lookup, p2sh_lookup=p2sh_lookup)
tx2.bad_signature_count()
tx2.as_hex() # is the raw hex of the totally signed transaction
print(tx.as_hex())
print("")
print("N. bad signatures: %s" % tx.bad_signature_count() )

