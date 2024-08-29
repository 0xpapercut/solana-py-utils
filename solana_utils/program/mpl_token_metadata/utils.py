from solders.pubkey import Pubkey

from .constants import MPL_TOKEN_METADATA_PROGRAM_ID

PREFIX = b"metadata"

def find_metadata_account(mint: Pubkey):
    seeds = [bytes(PREFIX), bytes(MPL_TOKEN_METADATA_PROGRAM_ID), bytes(mint)]
    return Pubkey.find_program_address(seeds, MPL_TOKEN_METADATA_PROGRAM_ID)
