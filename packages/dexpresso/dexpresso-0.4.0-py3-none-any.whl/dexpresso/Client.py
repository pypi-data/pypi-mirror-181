from .Web3Client import Web3Client
from .Configs import WEB3_COMPATIBLE_NETWORKS, ZKSYNC_ONE_NETWORKS


def get_client(network_obj, owner_address: str):
    if network_obj in WEB3_COMPATIBLE_NETWORKS:
        return Web3Client(network_obj, owner_address)
    elif network_obj in ZKSYNC_ONE_NETWORKS:
        raise "ZkSync v1 only supports Easy Client"
