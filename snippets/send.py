from bitcoin.bci import *
from bitcoin.transaction import *
import pprint
import requests
from cryptocorp import *
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
sub_public_wallets = [sub_wallet(chainPaths[i],public_wallets[i]) for i in range(len(chainPaths))]
sub_public_keys = [bip32_extract_key(key) for key in sub_public_wallets]

# You must not specify an outputChainPaths if the destination is not a p2sh address
outputChainPaths = "[null]" 

# address = "3Bi36w9RZHmibi1ip7ud9dvtpDt59ij7GC"
# inputScripts = ['5221033cb2f8b318f4c14e42cbe20cb365b2017d28bc557b0dde9eca2fbe8d3c9ed1982102e680e729a24923c09db6f958363b0416bc13970008ab7b925b2f2aa410e6b0a72102208fa0a00d6b9ae56f7cc137a021d03ae294d39242d64322f69bdc785853ba6453ae']
keychainId = str(data['chainid'])
script = mk_multisig_script(sub_public_keys,2,3)
address = scriptaddr(script)

sub_private_wallets = [sub_wallet(chainPaths[i],private_wallets[i]) for i in range(len(private_wallets))]
sub_private_keys = [bip32_extract_key(key) for key in sub_private_wallets]
# chiavi controllate

"""
Transaction {
    bytes (string): the serialized partial transaction
    inputScripts (array[string]) = an array of the input scripts (redeem scripts) associated with each input
    inputTransactions (array[string]): the input transactions raw hex
    chainPaths (array[string]): the chain paths for each input, or null if an input is not in the oracle controlled wallet
    outputChainPaths (array[string], optional): the chain paths for each output, or null if an input is not in the oracle controlled wallet
} 
"""
# Fetching unspent outputs relative to the address
h = history(address)
outs = [{'value': 10000, 'address': '1GRF5cmvAqQPNVPRHe1TpMZGS1mYFHFQHu'}] 
transaction = mktx(h, outs)
# checked: it seems correct but it gives "BAD SIGN" Warning. Probably because is not signed.


# this raw transaction is unsigned. Cryptocorp requires it to be signed on our part.
# The transaction must be signed.
# choosing the private key which will sign:
private_key = sub_private_keys[0]
# * multisign            : (tx, i, script, privkey) -> signature
# * apply_multisignatures: (tx, i, script, sigs) -> tx with index i signed with 
# >     bytes (string): the serialized partial transaction


script_signature = multisign(transaction,0,script,private_key) # signing the script(s)

# It is important to note that the index refer to the ordinal inside this transaction not to the ordinal 
# inside the source transaction. 

partially_signed_transaction = apply_multisignatures(transaction, 2, script, script_signature)

# I completely sign the transaction. Just to debug
private_key2 = sub_private_keys[1]

script_signature2 = multisign(transaction,0,script,private_key2) # signing the script(s)

completely_signed_transaction = apply_multisignatures(transaction, 0, script, script_signature)

#
# >    inputScripts (array[string]) = an array of the input scripts (redeem scripts) associated with each input
inputScripts = [script f for i in h]
# >    inputTransactions (array[string]): the input transactions raw hex
unspent_outputs = unspent(address)
tx_ids = []
for f in unspent_outputs: tx_ids.append(f['output'][0:64])

inputTransactions = [fetchtx(tx) for tx in tx_ids]

headers = {'content-type': 'application/json'}
payload = {"walletAgent": str(data['payload']['walletAgent']), "transaction": {"bytes" :  partially_signed_transaction , "inputScripts" : inputScripts, "inputTransactions" : inputTransactions, "masterKeys": masterKeys, "chainPaths" : chainPaths},"verifications": { "otp": "123456", "code": "234567" }}
pp.pprint(payload)
command = "keychains"
apiurl = "https://s.digitaloracle.co" # sandbox URL
requrl = apiurl + "/" + command + "/" + keychainId + "/transactions"
r = requests.post(requrl, data=json.dumps(payload), headers=headers)
pp.pprint(r.text)
