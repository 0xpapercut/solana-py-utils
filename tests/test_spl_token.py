import pytest
from solders.pubkey import Pubkey
from .conftest import client
from solana_utils.program.spl_token.state import Mint

from spl.token._layouts import MINT_LAYOUT

@pytest.fixture
def sample_mint_account_info(client):
    mint = Pubkey.from_string('DfdYHHPhdVswdDESPHuegdBexBsvynexJCAErk8Qpump')
    return client.get_account_info(mint).value

def test_mint_account_parse(sample_mint_account_info):
    print([x for x in sample_mint_account_info.data])
    print(len(sample_mint_account_info.data))
    print(Mint.parse(sample_mint_account_info.data))
    # print(MINT_LAYOUT.parse(sample_mint_account_info.data))
