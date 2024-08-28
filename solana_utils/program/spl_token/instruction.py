from enum import IntEnum
from construct import (
    Int8ul,
    Int64ul,
    Struct,
    Switch,
)
from ...construct import Pubkey

TransferInstruction = Struct("amount" / Int64ul)
TransferCheckedInstruction = Struct("amount" / Int64ul, "decimals" / Int8ul)

InitializeAccountInstruction = Struct()
InitializeAccount2Instruction = Struct("owner" / Pubkey)
InitializeAccount3Instruction = Struct("owner" / Pubkey)

class SplTokenDiscriminant(IntEnum):
    TRANSFER = 3
    TRANSFER_CHECKED = 12
    INITIALIZE_ACCOUNT = 1
    INITIALIZE_ACCOUNT2 = 16
    INITIALIZE_ACCOUNT3 = 18

SplTokenInstruction = Struct(
    "discriminant" / Int8ul,
    "instruction" / Switch(lambda ctx: ctx.discriminant, {
        SplTokenDiscriminant.INITIALIZE_ACCOUNT: InitializeAccountInstruction,
        SplTokenDiscriminant.INITIALIZE_ACCOUNT2: InitializeAccount2Instruction,
        SplTokenDiscriminant.INITIALIZE_ACCOUNT3: InitializeAccount3Instruction,
        SplTokenDiscriminant.TRANSFER: TransferInstruction,
        SplTokenDiscriminant.TRANSFER_CHECKED: TransferCheckedInstruction,
    })
)
