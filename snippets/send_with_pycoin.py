
# -*- coding: utf-8 -*-
from pycoin.encoding import wif_to_secret_exponent
from pycoin.convention import tx_fee
from pycoin.tx.Spendable import Spendable
from pycoin.tx.Tx import Tx
from pycoin.tx.tx_utils import *
from pycoin.tx.TxOut import TxOut, standard_tx_out_script
from pycoin.tx.pay_to import build_hash160_lookup, build_p2sh_lookup
from pycoin.services.blockr_io import *
from pycoin.key import Key

#from pycoin.services.blockchain_info import *

from pycoin.tx.pay_to import ScriptMultisig
from pycoin.tx.pay_to import address_for_pay_to_script, build_hash160_lookup, build_p2sh_lookup
from pycoin.serialize import b2h
from pycoin.key.BIP32Node import BIP32Node
import pprint
# this version uses pycoin lib.
# the first part just to verify that I can produce address and script

result_address = '3Bi36w9RZHmibi1ip7ud9dvtpDt59ij7GC'
result_script = '5221033cb2f8b318f4c14e42cbe20cb365b2017d28bc557b0dde9eca2fbe8d3c9ed1982102e680e729a24923c09db6f958363b0416bc13970008ab7b925b2f2aa410e6b0a72102208fa0a00d6b9ae56f7cc137a021d03ae294d39242d64322f69bdc785853ba6453ae'
chain_file = "results"
data = json.load(open((chain_file + ".json"), "r"))
private_wallets = json.load(open((chain_file + ".mseks.json"), "r"))
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(data)
masterKeys = data['keys'] #remember that cryptocorp's extended public key goes last
public_wallets = masterKeys 
# To obtain the redeem script and the p2sh address we need ALL the public keys involved

public_wallets.extend(data['cryptocorp_MPEK'])
chainPaths = ["0/0/7","0/0/7","0/0/7"]

masterbip32nodes = [Key.from_text(i) for i in public_wallets]

sub_bip32_nodes = [BIP32Node.subkey_for_path(masterbip32nodes[i], chainPaths[i]) for i in range(len(chainPaths))]

script_encoded = ScriptMultisig(n=2, sec_keys=[key.sec() for key in sub_bip32_nodes]).script()


script = b2h(script_encoded)
if script == result_script: print ('Yahooooooooo')




address = address_for_pay_to_script(script_encoded)
if address == result_address: print ('Yahooooooooo')

spendables = spendables_for_address(address)

tx = create_tx(spendables,["3J1GkczUWxxf5JfB5vVzRfFVBBWddotHZ5"], fee="standard")
# raw hex not-signed transaction

tx.as_hex()
# to sign the transaction I need the sub_private keys

masterBip32PrivateNodes = [Key.from_text(i) for i in private_wallets] #list of Bip32 node objects
subBip32PrivateNodes = [BIP32Node.subkey_for_path(masterBip32PrivateNodes[i], chainPaths[i]) for i in range(len(masterBip32PrivateNodes))] # subnodes

"""
# beginning part totally signed
privateSubKeysObjectsSecret_exponents = [Key.secret_exponent(i) for i in subBip32PrivateNodes]
hash160_lookup = build_hash160_lookup(privateSubKeysObjectsSecret_exponents)
p2sh_lookup = build_p2sh_lookup([script_encoded])
tx_signed = tx.sign(hash160_lookup=hash160_lookup, p2sh_lookup=p2sh_lookup)
tx_signed.bad_signature_count() # checking if the signature process has worked
tx_signed.as_hex() # is the raw hex correctly signed transaction
# end part totally signed
"""


#let's try to partially sign the transaction


p2sh_lookup = build_p2sh_lookup([script_encoded])
subBip32PrivateNode = subBip32PrivateNodes[0] # I take only the first key object
privateSubKeysObjectsSecret_exponent = [subBip32PrivateNode.secret_exponent()]
hash160_lookup = build_hash160_lookup(privateSubKeysObjectsSecret_exponent)
tx_signed = tx.sign(hash160_lookup=hash160_lookup, p2sh_lookup=p2sh_lookup)
tx_signed.bad_signature_count() # checking if the signature process has worked
tx_signed.as_hex() # is the raw hex partially signed transaction

