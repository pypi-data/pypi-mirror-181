"""
-------------------------------------
-- Dexpresso.protocol: LazyClient.py --
-------------------------------------
Class DexpressoLazyClient is directly connected to web3 providers and Dexpresso backend.
It combines all the functionalities from Client.py and OfflineSigner.py:
    - creation, sign and submission of limit orders
    - querying information and configurations of different markets/networks
    - querying orderbooks/latestfills/userfills/userorders/...
"""
from decimal import Decimal
from typing import List
from .Configs import GeneralNetwork
from .Web3OfflineSigner import Web3OfflineSigner
from .Web3Client import Web3Client


class Web3EasyClient:
    client: Web3Client
    signer: Web3OfflineSigner

    def __init__(self, network_obj: GeneralNetwork, privkey: str):
        self.signer = Web3OfflineSigner(privkey)
        self.client = Web3Client(network_obj, self.signer.owner_address)

    async def authenticate(self, user_data=False, uuid=None):
        signed = self.signer.new_signed_login_message(self.client.network.chain_id, user_data, uuid)
        return await self.client.authenticate(signed)

    async def approve_dexpresso_contract(self, token: str, amount: Decimal):
        approve_tx_dict = self.client.approve_dexpresso_contract(token, amount)
        signed = self.signer.sign_transaction(approve_tx_dict)
        return await self.client.broadcast_to_blockchain(signed)

    def create_and_submit_order(self, market: str, side: str, price: Decimal, amount: Decimal, expiration: int, fee: Decimal):
        raw_dict = self.client.create_raw_order(market, side, price, amount, expiration, fee)
        signed = self.signer.sign_limit_order(raw_dict)
        return self.client.submit_order(signed)

    def get_markets_info(self, markets: List = None):
        return self.client.get_markets_info(markets)

    def get_markets_config(self, markets: List = None):
        return self.client.get_markets_config(markets)

    def get_markets_stats(self, markets: List = None):
        return self.client.get_markets_stats(markets)

    def get_order_book(self, market: str, side: str = None, page: int = None, per_page: int = None):
        return self.client.get_order_book(market, side, page, per_page)

    def get_all_user_orders(self, market: str = None, start_time: str = None, end_time: str = None, side: str = None,
                            page: int = None, per_page: int = None):
        return self.client.get_all_user_orders(market, start_time, end_time,  page, per_page)

    def get_user_order(self, order_id: int):
        return self.client.get_user_order(order_id)

    def cancel_all_user_orders(self, side: str = None, market: str = None):
        return self.client.cancel_all_user_orders(side, market)

    def cancel_user_order(self, order_id: int):
        return self.client.cancel_user_order(order_id)

    def get_latest_fills(self,  market: str, page: int = None, per_page: int = None):
        return self.client.get_latest_fills(market, page, per_page)

    def get_user_fills(self, market: str = None):
        return self.client.get_user_fills(market)
