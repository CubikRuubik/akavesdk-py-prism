from typing import List, Tuple, Optional
from eth_typing import HexAddress, HexStr
from web3 import Web3
from web3.contract import Contract
import json


class AccessManagerContract:
    """Python bindings for the AccessManager smart contract."""

    def __init__(self, web3: Web3, contract_address: HexAddress):
        """Initialize the AccessManager contract interface.

        Args:
            web3: Web3 instance
            contract_address: Address of the deployed AccessManager contract
        """
        self.web3 = web3
        self.contract_address = contract_address

        # Contract ABI from Go bindings (v0.4.4)
        self.abi = [
            {"inputs": [{"internalType": "address", "name": "storageAddress", "type": "address"}], "stateMutability": "nonpayable", "type": "constructor"},
            {"inputs": [], "name": "BucketNotFound", "type": "error"},
            {"inputs": [], "name": "FileDoesNotExist", "type": "error"},
            {"inputs": [], "name": "InvalidAddress", "type": "error"},
            {"inputs": [], "name": "NoDelegatedAccess", "type": "error"},
            {"inputs": [], "name": "NoPolicy", "type": "error"},
            {"inputs": [], "name": "NotBucketOwner", "type": "error"},
            {"anonymous": False, "inputs": [{"indexed": True, "internalType": "bytes32", "name": "fileId", "type": "bytes32"}, {"indexed": True, "internalType": "address", "name": "delegatee", "type": "address"}], "name": "AccessDelegated", "type": "event"},
            {"anonymous": False, "inputs": [{"indexed": True, "internalType": "bytes32", "name": "fileId", "type": "bytes32"}, {"indexed": True, "internalType": "address", "name": "delegatee", "type": "address"}], "name": "AccessRemoved", "type": "event"},
            {"anonymous": False, "inputs": [{"indexed": True, "internalType": "bytes32", "name": "fileId", "type": "bytes32"}, {"indexed": False, "internalType": "bool", "name": "isPublic", "type": "bool"}], "name": "PublicAccessChanged", "type": "event"},
            {"anonymous": False, "inputs": [{"indexed": True, "internalType": "bytes32", "name": "fileId", "type": "bytes32"}, {"indexed": True, "internalType": "address", "name": "policy", "type": "address"}], "name": "PolicySet", "type": "event"},
            {"inputs": [{"internalType": "bytes32", "name": "fileId", "type": "bytes32"}, {"internalType": "bool", "name": "isPublic", "type": "bool"}], "name": "changePublicAccess", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
            {"inputs": [{"internalType": "bytes32", "name": "fileId", "type": "bytes32"}, {"internalType": "address", "name": "delegatee", "type": "address"}], "name": "delegateAccess", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
            {"inputs": [{"internalType": "bytes32", "name": "fileId", "type": "bytes32"}], "name": "getFileAccessInfo", "outputs": [{"internalType": "address", "name": "", "type": "address"}, {"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"},
            {"inputs": [{"internalType": "bytes32", "name": "fileId", "type": "bytes32"}], "name": "getPolicy", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
            {"inputs": [{"internalType": "bytes32", "name": "fileId", "type": "bytes32"}, {"internalType": "address", "name": "user", "type": "address"}, {"internalType": "bytes", "name": "data", "type": "bytes"}], "name": "getValidateAccess", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"},
            {"inputs": [{"internalType": "bytes32", "name": "bucketId", "type": "bytes32"}, {"internalType": "address", "name": "user", "type": "address"}, {"internalType": "bytes", "name": "data", "type": "bytes"}], "name": "getValidateAccessToBucket", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"},
            {"inputs": [{"internalType": "bytes32", "name": "bucketId", "type": "bytes32"}, {"internalType": "address", "name": "user", "type": "address"}], "name": "isBucketOwnerOrDelegate", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"},
            {"inputs": [{"internalType": "bytes32", "name": "fileId", "type": "bytes32"}, {"internalType": "address", "name": "delegatee", "type": "address"}], "name": "removeAccess", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
            {"inputs": [{"internalType": "bytes32", "name": "bucketId", "type": "bytes32"}, {"internalType": "address", "name": "policyContract", "type": "address"}], "name": "setBucketPolicy", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
            {"inputs": [{"internalType": "bytes32", "name": "fileId", "type": "bytes32"}, {"internalType": "address", "name": "policyContract", "type": "address"}], "name": "setFilePolicy", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
            {"inputs": [{"internalType": "address", "name": "storageAddress", "type": "address"}], "name": "setStorageContract", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
            {"inputs": [], "name": "storageContract", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
        ]

        self.contract = web3.eth.contract(address=contract_address, abi=self.abi)

    def change_public_access(self, auth, file_id: bytes, is_public: bool) -> HexStr:
        """Changes the public access status of a file.

        Args:
            auth: Authentication object with address and key
            file_id: ID of the file
            is_public: Whether the file should be publicly accessible

        Returns:
            Transaction hash
        """
        from eth_account import Account

        function = self.contract.functions.changePublicAccess(file_id, is_public)
        tx_params = {
            'from': auth.address,
            'gas': 500000,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(auth.address),
        }
        tx = function.build_transaction(tx_params)
        if isinstance(auth.key, str):
            private_key_bytes = bytes.fromhex(auth.key.replace('0x', ''))
        else:
            private_key_bytes = auth.key
        signed_tx = Account.sign_transaction(tx, private_key_bytes)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()

    def change_public_access_simple(self, file_id: bytes, is_public: bool, from_address: HexAddress) -> None:
        """Changes the public access status of a file (simple version that waits for receipt)."""
        tx_hash = self.contract.functions.changePublicAccess(file_id, is_public).transact({'from': from_address})
        self.web3.eth.wait_for_transaction_receipt(tx_hash)

    def delegate_access(self, auth, file_id: bytes, delegatee: HexAddress) -> HexStr:
        """Delegates access to a file for a specific address.

        Args:
            auth: Authentication object with address and key
            file_id: ID of the file
            delegatee: Address to delegate access to

        Returns:
            Transaction hash
        """
        from eth_account import Account

        function = self.contract.functions.delegateAccess(file_id, delegatee)
        tx_params = {
            'from': auth.address,
            'gas': 500000,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(auth.address),
        }
        tx = function.build_transaction(tx_params)
        if isinstance(auth.key, str):
            private_key_bytes = bytes.fromhex(auth.key.replace('0x', ''))
        else:
            private_key_bytes = auth.key
        signed_tx = Account.sign_transaction(tx, private_key_bytes)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()

    def remove_access(self, auth, file_id: bytes, delegatee: HexAddress) -> HexStr:
        """Removes delegated access for an address.

        Args:
            auth: Authentication object with address and key
            file_id: ID of the file
            delegatee: Address to remove access from

        Returns:
            Transaction hash
        """
        from eth_account import Account

        function = self.contract.functions.removeAccess(file_id, delegatee)
        tx_params = {
            'from': auth.address,
            'gas': 500000,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(auth.address),
        }
        tx = function.build_transaction(tx_params)
        if isinstance(auth.key, str):
            private_key_bytes = bytes.fromhex(auth.key.replace('0x', ''))
        else:
            private_key_bytes = auth.key
        signed_tx = Account.sign_transaction(tx, private_key_bytes)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()

    def set_bucket_policy(self, auth, bucket_id: bytes, policy_contract: HexAddress) -> HexStr:
        """Sets the policy contract for a bucket.

        Args:
            auth: Authentication object with address and key
            bucket_id: ID of the bucket
            policy_contract: Address of the policy contract

        Returns:
            Transaction hash
        """
        from eth_account import Account

        function = self.contract.functions.setBucketPolicy(bucket_id, policy_contract)
        tx_params = {
            'from': auth.address,
            'gas': 500000,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(auth.address),
        }
        tx = function.build_transaction(tx_params)
        if isinstance(auth.key, str):
            private_key_bytes = bytes.fromhex(auth.key.replace('0x', ''))
        else:
            private_key_bytes = auth.key
        signed_tx = Account.sign_transaction(tx, private_key_bytes)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()

    def set_file_policy(self, auth, file_id: bytes, policy_contract: HexAddress) -> HexStr:
        """Sets the policy contract for a file.

        Args:
            auth: Authentication object with address and key
            file_id: ID of the file
            policy_contract: Address of the policy contract

        Returns:
            Transaction hash
        """
        from eth_account import Account

        function = self.contract.functions.setFilePolicy(file_id, policy_contract)
        tx_params = {
            'from': auth.address,
            'gas': 500000,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(auth.address),
        }
        tx = function.build_transaction(tx_params)
        if isinstance(auth.key, str):
            private_key_bytes = bytes.fromhex(auth.key.replace('0x', ''))
        else:
            private_key_bytes = auth.key
        signed_tx = Account.sign_transaction(tx, private_key_bytes)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()

    def set_storage_contract(self, auth, storage_address: HexAddress) -> HexStr:
        """Sets the storage contract address.

        Args:
            auth: Authentication object with address and key
            storage_address: Address of the storage contract

        Returns:
            Transaction hash
        """
        from eth_account import Account

        function = self.contract.functions.setStorageContract(storage_address)
        tx_params = {
            'from': auth.address,
            'gas': 500000,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(auth.address),
        }
        tx = function.build_transaction(tx_params)
        if isinstance(auth.key, str):
            private_key_bytes = bytes.fromhex(auth.key.replace('0x', ''))
        else:
            private_key_bytes = auth.key
        signed_tx = Account.sign_transaction(tx, private_key_bytes)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()

    def get_validate_access(self, file_id: bytes, user: HexAddress, data: bytes) -> bool:
        """Validates access for a user to a file.

        Args:
            file_id: ID of the file
            user: Address of the user
            data: Additional data for validation

        Returns:
            True if the user has access, False otherwise
        """
        return self.contract.functions.getValidateAccess(file_id, user, data).call()

    def get_validate_access_to_bucket(self, bucket_id: bytes, user: HexAddress, data: bytes) -> bool:
        """Validates access for a user to a bucket.

        Args:
            bucket_id: ID of the bucket
            user: Address of the user
            data: Additional data for validation

        Returns:
            True if the user has access, False otherwise
        """
        return self.contract.functions.getValidateAccessToBucket(bucket_id, user, data).call()

    def is_bucket_owner_or_delegate(self, bucket_id: bytes, user: HexAddress) -> bool:
        """Checks if user is bucket owner or delegate.

        Args:
            bucket_id: ID of the bucket
            user: Address to check

        Returns:
            True if the user is the owner or a delegate
        """
        return self.contract.functions.isBucketOwnerOrDelegate(bucket_id, user).call()

    def get_file_access_info(self, file_id: bytes) -> Tuple[HexAddress, bool]:
        """Gets access information for a file.

        Args:
            file_id: ID of the file

        Returns:
            Tuple containing (policy contract address, is public)
        """
        return self.contract.functions.getFileAccessInfo(file_id).call()

    def get_policy(self, file_id: bytes) -> HexAddress:
        """Gets the policy contract address for a file.

        Args:
            file_id: ID of the file

        Returns:
            Address of the policy contract
        """
        return self.contract.functions.getPolicy(file_id).call()

    def get_storage_contract(self) -> HexAddress:
        """Gets the address of the associated storage contract.

        Returns:
            Address of the storage contract
        """
        return self.contract.functions.storageContract().call()


def new_access_manager(web3: Web3, contract_address: str) -> AccessManagerContract:
    return AccessManagerContract(web3, contract_address)


def deploy_access_manager(web3: Web3, account, storage_address: str) -> Tuple[str, str]:
    raise NotImplementedError("AccessManager deployment not yet implemented")
