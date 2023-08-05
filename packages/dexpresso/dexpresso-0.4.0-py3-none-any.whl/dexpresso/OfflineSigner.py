from .Web3OfflineSigner import Web3OfflineSigner
from .Configs import WEB3_COMPATIBLE_NETWORKS, ZKSYNC_ONE_NETWORKS


def get_offline_signer(network_obj, privkey: str):
    if network_obj in WEB3_COMPATIBLE_NETWORKS:
        return Web3OfflineSigner(privkey)
    elif network_obj in ZKSYNC_ONE_NETWORKS:
        raise "ZkSync v1 only supports Easy Client"
