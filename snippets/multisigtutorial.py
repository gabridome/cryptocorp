from pycoin.key import Key
from pycoin.serialize import h2b
from pycoin.tx import Tx, TxIn, TxOut, SIGHASH_ALL, tx_utils
from pycoin.tx.TxOut import standard_tx_out_script

from pycoin.tx.pay_to import ScriptMultisig, ScriptPayToPublicKey, ScriptNulldata
from pycoin.tx.pay_to import address_for_pay_to_script, build_hash160_lookup, build_p2sh_lookup
from pycoin.tx.pay_to import script_obj_from_address, script_obj_from_script

# Set up of the variables N is the number of required* keys
# M is the number of possibly capable keys
N, M = 4, 6

# list of keys build from secret exponents 1 to M +1
keys = [Key(secret_exponent=i) for i in range(1, M+1)]
# keys as they appear:
print("keys as it appears:")
for i in keys:
    print(i)

print("")
print("list of 'keys' wifs:")
print("")
for i in keys:
    print("Secret exponent  : %s " % i.secret_exponent())
    print("WIF  : %s " % i.wif())
    print("SEC  : %s " % i.sec_as_hex())
    print("")


# Building underlying script to redem the funds with N signatures out of M
underlying_script = ScriptMultisig(n=N, sec_keys=[key.sec() for key in keys[:M]]).script()
# I hash the script and transform it into a p2sh address
address = address_for_pay_to_script(underlying_script)
print(address)
# Filling up the new created address with the fake coinbase transaction. No signature rquired.
# Very important part. When you move funds to a p2sh address you write a special scriptPubKey:
# Instead of: OP_DUP OP_HASH160 <PubkeyHash> OP_EQUALVERIFY OP_CHECKSIG
# your p2sh scriptPubKey will be:
# OP_HASH160 <hash(redeemScript)> OP_EQUAL
# standard_tx_out_script(address) gives the scriptPubKey for a given multisig address
script = standard_tx_out_script(address)
# Fake coinbase transaction to fill our p2sh address
# It it is a coinbase transaction we put in a newly constructed block.
tx_in = TxIn.coinbase_tx_in(script=b'')
print("TxIn: %s" %  tx_in.__str__())
tx_out = TxOut(1000000, script)
print("TxOut: %s" %  tx_out.__str__())
tx1 = Tx(version=1, txs_in=[tx_in], txs_out=[tx_out])
tx1.as_hex()
# we now have an UTXO redeemable by supplying the script and the required sigs.
# tx_utils.create_tx() allows to spend all the UTXO from the preavious tx to an arbitrary address.
tx2 = tx_utils.create_tx(tx1.tx_outs_as_spendable(), [keys[-1].address()])
# to split the input in each of the generated addresses
# tx2 = tx_utils.create_tx(tx1.tx_outs_as_spendable(), [keys[i].address() for i in range(len(keys))])
print("unsigned transaction:")
print("bad signatures: %s" % tx2.bad_signature_count())
print(tx2.as_hex())
for i in range(1, N+1):
    print("signining with key number: %s" % i)
    hash160_lookup = build_hash160_lookup([keys[i].secret_exponent()])
    p2sh_lookup = build_p2sh_lookup([underlying_script])
    tx2.sign(hash160_lookup=hash160_lookup,p2sh_lookup=p2sh_lookup)
    print(tx2.as_hex())
    print("This transactions have now : %s signature of %t necessary" % (i, N)) 
    print("bad signatures: %s" % tx2.bad_signature_count())
