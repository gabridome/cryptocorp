from bitcoin.bci import *
from bitcoin.transaction import *
import pprint
import requests
data = json.load(open("results.json", "r"))
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(data)
chainPaths = ["0/0/7"]
outputChainPaths = ["0/1/7"]
keychainId = str(data['chainid'])
address = "3Bi36w9RZHmibi1ip7ud9dvtpDt59ij7GC"
inputScripts = ['5221033cb2f8b318f4c14e42cbe20cb365b2017d28bc557b0dde9eca2fbe8d3c9ed1982102e680e729a24923c09db6f958363b0416bc13970008ab7b925b2f2aa410e6b0a72102208fa0a00d6b9ae56f7cc137a021d03ae294d39242d64322f69bdc785853ba6453ae']

# Fetching unspent inputs relative to the address
unspent_outputs = unspent(address)
# From this I estract the hash of the transactions..
tx_ids = []
for f in unspent_outputs: tx_ids.append(f['output'][0:64])

txs_raw_hex = [fetchtx(tx) for tx in tx_ids]

unspents = []
for f in unspent_outputs: unspents.append(f['output'])

bytes = mktx(unspents, "1GRF5cmvAqQPNVPRHe1TpMZGS1mYFHFQHu:10000")
headers = {'content-type': 'application/json'}
payload = {"walletAgent": str(data['payload']['walletAgent']), "transaction": {"bytes" :  bytes , "inputScripts" : inputScripts, "inputTransactions" : txs_raw_hex,"chainPaths" : chainPaths,  "outputChainPaths" : outputChainPaths },"verifications": { "otp": "123456", "code": "234567" }}
pp.pprint(payload)
command = "keychains"
apiurl = "https://s.digitaloracle.co" # sandbox URL
requrl = apiurl + "/" + command + "/" + keychainId + "/transactions"
r = requests.post(requrl, data=json.dumps(payload), headers=headers)
