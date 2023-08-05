"""
-------------------------------------
-- Dexpresso.protocol: Client.py --
-------------------------------------
Class DexpressoClient is directly connected to web3 providers and Dexpresso backend.
It handles following functionalities:
    - creation and submition of limit orders
    - querying information and configurations of different markets/networks
    - querying orderbooks/latestfills/userfills/userorders/...
"""
import asyncio
import json
from decimal import Decimal
from hexbytes import HexBytes
from web3 import Web3
from web3.eth import AsyncEth
from web3.net import AsyncNet

from .Configs import DEXPRESSO_SWAPPER_CONTRACT_ADDRESS, GeneralNetwork
from .GeneralClient import GeneralClient


class Web3Client(GeneralClient):
    web3: Web3
    owner_address: str
    _latest_uuid: str
    approve_gas: int
    average_block_time: Decimal

    def __init__(self, network_obj: GeneralNetwork, owner_address: str, **kwargs):
        super().__init__(network_obj, owner_address)
        self.web3 = Web3(Web3.AsyncHTTPProvider(network_obj.provider_url),
                         modules={'eth': (AsyncEth,), 'net': (AsyncNet,)}, middlewares=[])
        self.approve_gas = 70000
        """ Estimate average block time --> needed for expiration calculation """
        now_block_number = asyncio.run(self.web3.eth.get_block_number()) - 10
        now_block = self.web3.eth.get_block("latest", now_block_number)
        then_block = self.web3.eth.get_block("latest", now_block_number - 500)
        self.average_block_time = Decimal(now_block['timestamp'] - then_block['timestamp']) / Decimal(500)

    async def approve_dexpresso_contract(self, token: str, amount: Decimal):
        gas = self.approve_gas
        nonce = await self.web3.eth.getTransactionCount(self.owner_address)
        abi_dict = [{"constant": False, "inputs": [{"name": "_spender", "type": "address"},
                                                   {"name": "_value", "type": "uint256"}],
                     "name": "approve", "outputs": [{"name": "success", "type": "bool"}], "payable": False,
                     "stateMutability": "nonpayable", "type": "function"},
                    {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}],
                     "payable": False, "stateMutability": "view", "type": "function"},
                    {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf",
                     "outputs": [{"name": "balance", "type": "uint256"}], "payable": False, "stateMutability": "view",
                     "type": "function"}
                    ]
        erc20_contract = self.web3.eth.contract(
            Web3.toChecksumAddress(token),
            abi=abi_dict)
        decimals = await erc20_contract.functions.decimals().call()
        approve_tx_dict = await erc20_contract.functions.approve(
            DEXPRESSO_SWAPPER_CONTRACT_ADDRESS,
            int(Decimal(decimals) * Decimal(amount))
        ).buildTransaction(
            {
                'nonce': nonce,
                'gas': gas,
                'gasPrice': self.web3.eth.gas_price,
                'from': self.owner_address,
                'value': 0,
                'chainId': self.network.chain_id
            }
        )
        return approve_tx_dict

    def create_raw_order(self, market: str, side: str, price: Decimal, amount: Decimal, expiration: int, fee: Decimal):
        if side not in ['b', 's', 'buy', 'sell']:
            raise "Given side is not valid!\n" \
                  "Available options: 1) 'buy' or 'b',  2) 's' or 'sell'"
        if market not in self.network.markets:
            raise f"Given market is not available in this network!\n" \
                  f"Available options: {self.network.markets.keys()}"
        if side in ['b', 'buy']:
            selling_token = self.network.markets[market]["quote_asset"]["address"]
            buying_token = self.network.markets[market]["base_asset"]["address"]
            spending_amount = int(amount * price * Decimal(self.network.markets[market]["quote_asset"]["decimals"]))
            receiving_amount = int(amount * Decimal(self.network.markets[market]["base_asset"]["decimals"]))
        else:
            selling_token = self.network.markets[market]["base_asset"]["address"]
            buying_token = self.network.markets[market]["quote_asset"]["address"]
            spending_amount = int(amount * Decimal(self.network.markets[market]["base_asset"]["decimals"]))
            receiving_amount = int(amount * price * Decimal(self.network.markets[market]["quote_asset"]["decimals"]))
        latest_block = self.web3.eth.get_block_number()
        valid_until = latest_block + int(Decimal(expiration) / self.average_block_time)
        raw_hex = hex(self.network.chain_id)[2:].zfill(64)
        raw_hex += selling_token[2:].zfill(64)
        raw_hex += buying_token[2:].zfill(64)
        raw_hex += hex(spending_amount)[2:].zfill(64)
        raw_hex += hex(receiving_amount)[2:].zfill(64)
        raw_hex += hex(valid_until)[2:].zfill(64)
        final_dict = {
            'tx': {
                'accountId': self.owner_address,
                'tokenSell': selling_token,
                'tokenBuy': buying_token,
                'ratio': [str(spending_amount), str(receiving_amount)],
                'validUntil': valid_until,
                'raw_data': raw_hex,
            },
            "market": market,
            "amount": str(int(amount * Decimal(self.network.markets[market]["base_asset"]["decimals"]))),
            "price": str(float(price)),
            "type": "l"
        }
        return final_dict

    async def broadcast_to_blockchain(self, signed_tx: HexBytes):
        return self.web3.eth.send_raw_transaction(transaction=signed_tx)
