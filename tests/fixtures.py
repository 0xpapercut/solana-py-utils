import os
import pytest

from solana.rpc.api import Client

from solders.signature import Signature
from solders.pubkey import Pubkey

@pytest.fixture(scope="session")
def client() -> Client:
    return Client(os.environ['SOLANA_HTTP'])

@pytest.fixture(scope="session")
def sample_create_metadata_accountv3_transaction(client):
    signature = Signature.from_string('32DnWd5CdJgkShpf3L9Pd6s4PfrjH7NLg1katRcHq5pkQpyLdfTwaAo5cdk6D3P3HtZTwfg1xzvh7QAdgDTKcZs')
    return client.get_transaction(signature, encoding='base64')

@pytest.fixture(scope="session")
def sample_metadata_account(client):
    address = Pubkey.from_string('FXEpSY3ygURNNK5MxRDcEMRygzdjGZDfE48FUm6SpoZa')
    return client.get_account_info(address, encoding='base64')

@pytest.fixture(scope="session")
def sample_raydium_swap_confirmed_transaction(client: Client):
    signature = Signature.from_string('2JvxmigRaVSszUdVhXBNhkLQh1sxDQeB7MKLKNsk1tShdMEPLTqEkr3dshAz5zrSopRrPZsbhkwtnqJT7dHnpgBY')
    return client.get_transaction(signature, max_supported_transaction_version=0, encoding="base64").value
