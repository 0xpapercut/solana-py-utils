from dataclasses import dataclass
from solders.pubkey import Pubkey
from solders.transaction_status import UiTransactionTokenBalance

@dataclass
class TokenAccount:
    mint: Pubkey
    address: Pubkey
    owner: Pubkey

    @classmethod
    def from_token_balance(cls, token_balance: UiTransactionTokenBalance, account_keys: list[Pubkey]) -> 'TokenAccount':
        return cls(
            mint=token_balance.mint,
            address=account_keys[token_balance.account_index],
            owner=token_balance.owner
        )
