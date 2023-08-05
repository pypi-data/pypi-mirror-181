import os
from decimal import Decimal

from dexpresso.EasyClient import get_easy_client
from dexpresso import Configs

os.environ['ZK_SYNC_LIBRARY_PATH'] = os.path.join(os.path.dirname(__file__),
                                                  'zksync_lib/zks-crypto-x86_64-unknown-linux-gnu.so')

wallet_privkey = 'RAW_PRIVKEY_HEX'

print("creating client . . .")
ezcl_zk = get_easy_client(Configs.ZkSyncOneTestnet, wallet_privkey)

print("getting markets info . . . ")
res = ezcl_zk.get_markets_info()
print("markets info:\n", res)

print("getting markets stats . . . ")
res = ezcl_zk.get_markets_stats()
print("markets stats:\n", res)

print("Logging into Dexpresso . . . ")
res = ezcl_zk.authenticate()
access_token = res["access_token"]
print("auth. result:\n", res)

print("Submitting order using the JWT token from login . . .")
res = ezcl_zk.create_and_submit_order(
    'ETH-USDC',
    'buy',
    Decimal(1025.56),
    Decimal(0.01),
    3600,
    Decimal(0.01)
)

print("Order submission result:\n", res)

