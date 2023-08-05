# Dexpresso Python SDK 
A python SDK for better interactions with Dexpresso decentralized exchange (DEX).

## Quickstart

### Installation

Dexpresso-SDK can be installed (preferably in a virtualenv) using `pip` as follows:

`$ pip install dexpresso`

#### **Note**

If you run into problems during installation, you might have a broken environment. See the troubleshooting guide to setting up a clean environment.

### Example Usage
Following examples submit a limit order on ZkSyncV1 testnet (on Goerli) and Fantom Mainnet networks.
For the start, let's import `get_easy_client` method from `dexpresso`, which provides easy interactions with Dexpresso without getting involved into details. The `Configs` is required to pass network configurations to the client in a safer manner (the provider URL and chainId are hardcoded to prevent mistakes): 
```
import os
from decimal import Decimal

from dexpresso.EasyClient import get_easy_client
from dexpresso import Configs
```
The following line is only required if you are about to use zkSyncV1 network. The `ZK_SYNC_LIBRARY_PATH` is required by the [zkSync's python library](https://docs.zksync.io/api/sdk/python/tutorial/) itself and can be downloaded from [here](https://github.com/zksync-sdk/zksync-crypto-c/releases):
```
os.environ['ZK_SYNC_LIBRARY_PATH'] = os.path.join(os.path.dirname(__file__),
                                                  'zksync_lib/zks-crypto-x86_64-unknown-linux-gnu.so')
```
Now the easy client object can be instantiated by specifying the chosen network and the private key:
```
wallet_privkey = 'RAW_PRIVKEY_HEX'

#### Get network object for zksync_v1
net_obj = Configs.ZkSyncOneTestnet()
#### or get network object for Fantom
net_obj = Configs.FantomMainnet()

print("creating client . . .")
ezcl = get_easy_client(net_obj, wallet_privkey)
```
The rest of the code are independent of what network you use. In the followings, we get markets info and stats, respectively. 
```
print("getting markets info . . . ")
res = ezcl.get_markets_info()
print("markets info:\n", res)

print("getting markets stats . . . ")
res = ezcl.get_markets_stats()
print("markets stats:\n", res)
```
Before submitting orders or being able to get account's order lists and history, you are required to prove to the Dexpresso that you own the private key of the address. Therefore, you need to sign a custom message and send it to Dexpresso. The `authenticate` function does all that for simplicity: 
```
print("Logging into Dexpresso . . . ")
res = ezcl.authenticate()
access_token = res["access_token"]
print("auth. result:\n", res)
```
For submitting an order, the `easy_client` takes care of all required signatures and securely submits it via Dexpresso's API interface:
```
print("Submitting order using the JWT token from login . . .")
res = ezcl.create_and_submit_order(
    'ETH-USDC',
    'buy',
    Decimal(1025.56),
    Decimal(0.01),
    3600,
    Decimal(0.01)
)

print("Order submission result:\n", res)

```

### Dexpresso Python SDK Structure
Since Dexpresso is a decentralized exchange (DEX) working on multiple blockchains, this library/SDK depends on a connection to the blockchain fullnode that user wishes to place orders on. To eliminate any complexity while using this python SDK, we provide multiple **"pre-configured"** providers on main supported networks. Therefore, you do not need to build and set up a working environment with the underlying blockchain (_i.e. Web3.py for ETH-like networks or Tronpy for Tron blockchain_). 

The following diagram shows two ways of using `Dexpresso.py`: 1) **Normal** flow, and 2) **Easy** flow.



                      ┌─────                                     ┌──────
                      │                                          │
                      │ ┌────────────┐                           │ ┌───────────┐
                      │ │ Configs.py │                           │ │ Client.py │
                      │ └────────────┘                           │ └───────────┘
          Offline  ───┤                              Online   ───┤
       (No Internet)  │ ┌──────────────────┐    (Internet Conn.) │ ┌───────────────┐
                      │ │ OfflineSigner.py │                     │ │ EasyClient.py │
                      │ └──────────────────┘                     │ └───────────────┘
                      │                                          │
                      └──────                                    └──────


                                  Normal Flow:                    Easy Flow:
                    ┌─────────────────────────────────────┐  ┌───────────────────┐
                    │                                     │  │                   │
                    │  ┌───────────┐ ┌──────────────────┐ │  │ ┌───────────────┐ │
                    │  │ Client.py │ │ OfflineSigner.py │ │  │ │ EasyClient.py │ │
                    │  └─────┬─────┘ └─────────┬────────┘ │  │ └───────┬───────┘ │
                    │        │                 │          │  │         │         │
                    │        │                 │          │  │         │         │
                    │  create order            │          │  │   create order    │
                    │        │  ────────────►  │          │  │         │         │
                    │        │                 │          │  │         │         │
                    │        │             Sign Order     │  │     sign order    │
                    │        │                 │          │  │         │         │
                    │        │  ◄────────────  │          │  │         │         │
                    │        │                 │          │  │   submit order    │
                    │  submit order            │          │  │         │         │
                    │        │                 │          │  │         │         │
                    │        │                 │          │  │         │         │
                    │                                     │  │                   │
                    └─────────────────────────────────────┘  └───────────────────┘



### Normal Flow:
This is the standard flow where many SDK users prefer to ensure their private assets (_private keys_) are always accessed **"Offline"**. To this end, we distinguished order creation process from signing the order. The `Client` class is responsible for `creating order` and `submitting` a signed order to the Dexpresso exchange. On the other hand, the `OfflineSigner` class takes user's private key to be able to sign created orders by `Client`, while being completely offline.
### Easy Flow:
In some cases, users may not be needing to completely separate and isolate creation and signature generation processes in their already developed projects. Therefore, we also provide an all-in-one class `EasyClient` that can handle entire process within one line of code. We note that the underlying functions and objects used to implement the `EasyClient` are the exact classes and methods from the **Normal Flow**, which ensure that not private asset of the user is in danger of being exposed outside of user's local device.

#### **Note**
Some networks, such as _"zkSync V1"_ are only implemented as `EasyClient`.




