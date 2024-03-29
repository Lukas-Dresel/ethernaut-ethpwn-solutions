#!/usr/bin/env python3

import argparse
import os
from pathlib import Path
import sys
from time import sleep
from ethpwn import *

parser = argparse.ArgumentParser()
parser.add_argument('proxy_addr', type=str)
parser.add_argument('--force', action='store_true', help="Force the exploit even if estimage_gas says it will fail")
ARGS = parser.parse_args()

context.log_level = 'DEBUG'

FILE_DIR = Path(__file__).parent.resolve()
solidity_includes = FILE_DIR.parent / 'solidity-includes'

compile_contracts([FILE_DIR / 'detection.sol'], import_remappings={
    'openzeppelin-contracts-08': solidity_includes / 'openzeppelin-contracts-0.8' / 'contracts',
})

dep_token = CONTRACT_METADATA['DoubleEntryPoint'].get_contract_at(ARGS.proxy_addr)
print(f"DoubleEntryPointToken contract is at {dep_token.address}")

vault = CONTRACT_METADATA['CryptoVault'].get_contract_at(dep_token.functions.cryptoVault().call())
print(f"CryptoVault contract is at {vault.address}")

legacy_token = CONTRACT_METADATA['LegacyToken'].get_contract_at(dep_token.functions.delegatedFrom().call())
print(f"LegacyToken contract is at {legacy_token.address}")

forta = CONTRACT_METADATA['Forta'].get_contract_at(dep_token.functions.forta().call())
print(f"Forta contract is at {forta.address}")


tx_hash, detection_bot = CONTRACT_METADATA['DetectionBot'].deploy(ARGS.proxy_addr, force=ARGS.force)
print(f"DetectionBot contract is at {detection_bot.address}")

sleep(1)
print(f"Registering detection bot ...")
transact(forta.functions.setDetectionBot(detection_bot.address), force=ARGS.force)
