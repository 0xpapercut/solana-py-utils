import os
import pytest
from pprint import pprint

from solana_utils.instruction import (
    StructuredInstruction,
    StructuredInstructions,
    flattened_compiled_instructions,
    get_main_instructions,
    get_inner_instructions,
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

def test_flattened_instructions(sample_raydium_swap_confirmed_transaction):
    flattened = flattened_compiled_instructions(sample_raydium_swap_confirmed_transaction)
    assert(len(flattened) == 13)

def test_structured_instructions(sample_raydium_swap_confirmed_transaction):
    # structured = StructuredInstruction.build_structured_instructions(sample_raydium_swap_confirmed_transaction)
    structured = StructuredInstructions.build(sample_raydium_swap_confirmed_transaction)
    assert(len(structured.instructions) == 5)
    flattened = structured.flattened()
    assert(len(flattened) == 13)
