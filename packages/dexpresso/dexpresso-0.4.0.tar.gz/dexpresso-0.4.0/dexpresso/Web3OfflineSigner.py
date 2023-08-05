"""
-------------------------------------
-- Dexpresso.protocol: Offline_signer.py --
-------------------------------------
Class OfflineSigner is responsible for generating valid signatures by employing user's private key.
The class does not need any connection to ensure security of user's private assets (it's a Cold module!).
"""
from typing import Dict

from eth_account import Account
from eth_keys import keys
from eth_account.messages import encode_defunct


class Web3OfflineSigner:
    privkey: str
    pubkey: str
    owner_address: str

    def __init__(self, privkey: str):
        self.privkey = privkey
        self.pubkey = keys.PrivateKey(bytes.fromhex(privkey)).public_key.to_bytes().hex()
        self.owner_address = Account.from_key(privkey).address

    def new_signed_login_message(self, chain_id: int, user_data=False, uuid=None):
        login_body = {
            'chain_id': chain_id,
            'address': self.owner_address,
            'signature': self.sign_message('Login to Dexpresso'),
            'user_data': user_data,
            'uuid': uuid or "",
        }
        return login_body

    def sign_message(self, message: str):
        msghash = encode_defunct(text=message)
        signature = Account.sign_message(msghash, self.privkey).signature.hex()
        return signature

    def sign_limit_order(self, order_dict: Dict):
        """ build hex data to be signed """
        msghash = encode_defunct(hexstr=f'0x{order_dict["tx"]["raw_data"]}')
        signature = Account.sign_message(msghash, self.privkey).signature.hex()
        order_dict['tx']['signature'] = {
            'signature': signature,
            'pubKey': self.pubkey
        }
        del order_dict['tx']['raw_data']
        return order_dict

    def sign_transaction(self, tx_dict: Dict):
        signed_approve_tx = Account.signTransaction(tx_dict, private_key=self.privkey)
        return signed_approve_tx.rawTransaction
