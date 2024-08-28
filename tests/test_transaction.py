import os
import pytest
import base58
from pprint import pprint

from solana_utils.instruction import (
    StructuredInstruction,
    StructuredInstructions,
    flattened_compiled_instructions,
    get_main_instructions,
    get_inner_instructions,
)
from solana_utils.transaction import (
    get_encoded_transaction_with_status_meta,
    get_signers,
)

from solders.signature import Signature
from solders.pubkey import Pubkey
from solders.transaction_status import EncodedConfirmedTransactionWithStatusMeta

from solana.rpc.api import Client

@pytest.fixture(scope="module")
def client() -> Client:
    return Client(os.environ['SOLANA_HTTP'])

@pytest.fixture(scope="module")
def sample_raydium_swap_confirmed_transaction(client: Client) -> EncodedConfirmedTransactionWithStatusMeta:
    signature = Signature.from_string('2JvxmigRaVSszUdVhXBNhkLQh1sxDQeB7MKLKNsk1tShdMEPLTqEkr3dshAz5zrSopRrPZsbhkwtnqJT7dHnpgBY')
    return client.get_transaction(signature, max_supported_transaction_version=0).value

def test_transaction_signers(sample_raydium_swap_confirmed_transaction):
    transaction = get_encoded_transaction_with_status_meta(sample_raydium_swap_confirmed_transaction)
    assert get_signers(transaction) == [Pubkey.from_string('3js2tEnPqZkVZdNmT1CLQ2sUK1RkiXFfi6TqJEZ66FcV')]
