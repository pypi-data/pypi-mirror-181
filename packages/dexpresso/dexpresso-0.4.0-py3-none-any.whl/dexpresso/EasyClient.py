from .Web3EasyClient import Web3EasyClient
from .ZkSyncOneEasyClient import ZkSyncOneEasyClient
from .Configs import WEB3_COMPATIBLE_NETWORKS, ZKSYNC_ONE_NETWORKS


def get_easy_client(network_obj, privkey: str):
    if network_obj in WEB3_COMPATIBLE_NETWORKS:
        return Web3EasyClient(network_obj, privkey)
    elif network_obj in ZKSYNC_ONE_NETWORKS:
        return ZkSyncOneEasyClient(network_obj, privkey)
    raise Exception(f'The class of {network_obj} not supported!')