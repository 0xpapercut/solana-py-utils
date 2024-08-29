import os
import pytest

from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient

from solders.signature import Signature
from solders.pubkey import Pubkey
from solders.account import Account

from solders.transaction_status import EncodedConfirmedTransactionWithStatusMeta
from solders.rpc.responses import GetTransactionResp

def encode():
    pass

def decode():
    pass

@pytest.fixture(scope="session")
def client() -> Client:
    return Client(os.environ['SOLANA_HTTP'])

@pytest.fixture(scope="session")
def async_client() -> Client:
    return AsyncClient(os.environ['SOLANA_HTTP'])

@pytest.fixture(scope="session")
def sample_create_metadata_accountv3_transaction(client: Client, request):
    key = 'sample_create_metadata_accountv3_transaction'
    value = request.config.cache.get(key, None)
    if value is not None:
        return GetTransactionResp.from_json(value).value

    signature = Signature.from_string('iytVJZqdAzmn6AsuX8crZSs2pojoqXiVYbtevtqtdMCVCHjBmNTPtjbuhFRXFAzKVmm2n5zrgf8rFSsFvanu5jf')
    transaction = client.get_transaction(signature, encoding='base64', max_supported_transaction_version=0)
    request.config.cache.set(key, transaction.to_json())
    return transaction.value


# @pytest.fixture(scope="session")
# def sample_create_metadata_accountv3_transaction(client: Client, request):
#     key = 'sample_create_metadata_accountv3_transaction'
#     value = request.config.cache.get(key, None)
#     if value is not None:
#         return GetTransactionResp.from_json(value).value

#     signature = Signature.from_string('32DnWd5CdJgkShpf3L9Pd6s4PfrjH7NLg1katRcHq5pkQpyLdfTwaAo5cdk6D3P3HtZTwfg1xzvh7QAdgDTKcZs')
#     transaction = client.get_transaction(signature, encoding='base64', max_supported_transaction_version=0)
#     request.config.cache.set(key, transaction.to_json())
#     return transaction.value

@pytest.fixture(scope="session")
def sample_metadata_account(client, request):
    key = 'sample_metadata_account'
    value = request.config.cache.get(key, None)
    if value is not None:
        return Account.from_json(value)

    address = Pubkey.from_string('FXEpSY3ygURNNK5MxRDcEMRygzdjGZDfE48FUm6SpoZa')
    account = client.get_account_info(address, encoding='base64').value
    request.config.cache.set(key, account.to_json())
    return account

@pytest.fixture(scope="session")
def sample_raydium_swap_confirmed_transaction(client: Client, request):
    key = 'sample_raydium_swap_confirmed_transaction'
    value = request.config.cache.get(key, None)
    if value is not None:
        return GetTransactionResp.from_json(value).value

    signature = Signature.from_string('2JvxmigRaVSszUdVhXBNhkLQh1sxDQeB7MKLKNsk1tShdMEPLTqEkr3dshAz5zrSopRrPZsbhkwtnqJT7dHnpgBY')
    transaction = client.get_transaction(signature, encoding='base64', max_supported_transaction_version=0)
    request.config.cache.set(key, transaction.to_json())
    return transaction.value

    # signature = Signature.from_string('2JvxmigRaVSszUdVhXBNhkLQh1sxDQeB7MKLKNsk1tShdMEPLTqEkr3dshAz5zrSopRrPZsbhkwtnqJT7dHnpgBY')
    # return client.get_transaction(signature, max_supported_transaction_version=0, encoding="base64").value
