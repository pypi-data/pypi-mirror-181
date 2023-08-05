"""
-------------------------------------
-- Dexpresso.protocol: configs.py --
-------------------------------------
Contains general/standard information and configurations of different blockchains.
We use different classes to provide an attribute-style configuration for better readability.
"""
from typing import Dict


class GeneralNetwork:
    chain_id: int
    provider_url: str
    dexpresso_contract = '0x'
    markets: Dict
    name: str


class EthereumMainnet(GeneralNetwork):
    chain_id = 1
    provider_url = 'https://rpc.ankr.com/eth'
    name = 'ethereum'


class EthereumTestnet(GeneralNetwork):
    chain_id = 5
    provider_url = 'https://rpc.ankr.com/eth_goerli'
    name = 'ethereum_goerli'


class ZkSyncTwoTestnet(GeneralNetwork):
    chain_id = 280
    provider_url = 'https://zksync2-testnet.zksync.dev'
    name = 'zksyncv2_goerli'


class FantomMainnet(GeneralNetwork):
    chain_id = 250
    provider_url = 'https://rpc.fantom.network'
    name = 'fantom'


class PolygonMainnet(GeneralNetwork):
    chain_id = 137
    provider_url = 'https://polygon-rpc.com'
    name = 'polygon'


class AvalancheMainnet(GeneralNetwork):
    chain_id = 43114
    provider_url = 'https://api.avax.network/ext/bc/C/rpc'
    name = 'avalanche'


class OptimismMainnet(GeneralNetwork):
    chain_id = 10
    provider_url = 'https://mainnet.optimism.io'
    name = 'optimism'


class ZkSyncOneNetwork(GeneralNetwork):
    zk_provider_url: str
    web3_provider_url: str

    @property
    def provider_url(self):
        raise "ZkSync network objects don't have one 'provider_url', " \
              "but two providers: 'zk_provider_url' and 'web3_provider_url'"


class ZkSyncOneMainnet(ZkSyncOneNetwork):
    chain_id = 1
    zk_provider_url = 'https://api.zksync.io/jsrpc'
    web3_provider_url = 'https://rpc.ankr.com/eth'
    name = 'zksyncv1'


class ZkSyncOneTestnet(ZkSyncOneNetwork):
    chain_id = 5
    zk_provider_url = 'https://goerli-api.zksync.io/jsrpc'
    web3_provider_url = 'https://rpc.ankr.com/eth_goerli'
    name = 'zksyncv1_goerli'


DEXPRESSO_API_URL = 'http://127.0.0.1:3004/api/v1'
DEXPRESSO_SWAPPER_CONTRACT_ADDRESS = "0x"
WEB3_COMPATIBLE_NETWORKS = [EthereumMainnet, EthereumTestnet, FantomMainnet, PolygonMainnet, OptimismMainnet,
                            ZkSyncTwoTestnet, AvalancheMainnet]
ZKSYNC_ONE_NETWORKS = [ZkSyncOneMainnet, ZkSyncOneTestnet]
