import pytest

from solana_utils.program.mpl_token_metadata.state import DataV2

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

from solana_utils.program.mpl_token_metadata.state import Metadata

from solders.signature import Signature
from solders.pubkey import Pubkey
from solders.transaction_status import EncodedConfirmedTransactionWithStatusMeta

from solana.rpc.api import Client

@pytest.fixture(scope="module")
def client() -> Client:
    return Client(os.environ['SOLANA_HTTP'])

@pytest.fixture
def sample_datav2_bytes():
    return bytes([10, 0, 0, 0, 84, 101, 115, 116, 32, 65, 115, 115, 101, 116, 3, 0, 0, 0, 84, 83, 84, 30, 0, 0, 0, 104, 116, 116, 112, 115, 58, 47, 47, 101, 120, 97, 109, 112, 108, 101, 46, 99, 111, 109, 47, 97, 115, 115, 101, 116, 46, 106, 115, 111, 110, 244, 1, 0, 0, 0])

@pytest.fixture(scope="module")
def sample_create_metadata_accountv3_transaction(client):
    signature = Signature.from_string('iytVJZqdAzmn6AsuX8crZSs2pojoqXiVYbtevtqtdMCVCHjBmNTPtjbuhFRXFAzKVmm2n5zrgf8rFSsFvanu5jf')
    return client.get_transaction(signature, max_supported_transaction_version=0, encoding='base58').value

@pytest.fixture
def sample_metadata_account(client):
    address = Pubkey.from_string('FXEpSY3ygURNNK5MxRDcEMRygzdjGZDfE48FUm6SpoZa')
    return client.get_account_info(address, encoding='base64')

def test_datav2_decode(sample_datav2_bytes):
    data = DataV2.parse(sample_datav2_bytes)

@pytest.fixture(scope="module")
def sample_create_metadata_accountv3_instruction(sample_create_metadata_accountv3_transaction):
    structured = StructuredInstructions.build(sample_create_metadata_accountv3_transaction, data_encoding='base58')
    return structured.instructions[3].inner_instructions[4]

def test_create_metadata_accountv3_instruction(sample_create_metadata_accountv3_instruction):
    from solana_utils.program.mpl_token_metadata.instruction import MplTokenMetadataInstruction
    print(MplTokenMetadataInstruction.parse(sample_create_metadata_accountv3_instruction.data))
    # print(sample_create_metadata_accountv3_instruction.data

def test_metadata_account_decode(sample_metadata_account):
    # data = sample_metadata_account.value.data
    # print(sample_metadata_account)
    # print(data)
    # print(Metadata.parse(data).data.name)
    pass
