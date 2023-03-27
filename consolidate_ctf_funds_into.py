#!/usr/bin/env python3

import sys
from ethpwn import *

#!/usr/bin/env python3

from web3 import Web3
from time import sleep

from ethpwn import context
from ethpwn.contract import CONTRACT_METADATA
from ethpwn.transactions import transfer_funds
from ethpwn.currency_utils import ether, wei

MY_WALLET = get_wallet_by_name('Laptop CTF Metamask')
assert MY_WALLET is not None

context.log_level = 'DEBUG'

context.connect_http()
context.default_from_addr = MY_WALLET.address
context.default_signing_key = MY_WALLET.private_key

print("Current balance of wallets:")
for address, wallet in config.GLOBAL_CONFIG['wallets'].items():
    balance = context.w3.eth.get_balance(wallet.address)
    print(f"{wallet.name} [{wallet.address}]: {balance} [ {context.w3.from_wei(balance, 'ether')} ether ]")

if len(sys.argv) == 2:
    target_wallet = get_wallet_by_name(sys.argv[1])
    assert target_wallet is not None, f"Could not find wallet {sys.argv[1]!r}"

    for address, wallet in config.GLOBAL_CONFIG['wallets'].items():
        if wallet.name == target_wallet.name:
            continue

        if ether(wallet.balance()) < 0.001:
            context.logger.info(f"Skipping {wallet.name} because it has {ether(wallet.balance())} < 0.001 ether")
            continue

        transfer_funds(address, target_wallet.address, None, private_key=wallet.private_key)