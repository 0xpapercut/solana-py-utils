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

class SplTokenInstructionDiscriminant(IntEnum):
    TRANSFER = 3
    TRANSFER_CHECKED = 12
    INITIALIZE_ACCOUNT = 1
    INITIALIZE_ACCOUNT2 = 16
    INITIALIZE_ACCOUNT3 = 18

SplTokenInstruction = Struct(
    "discriminant" / Int8ul,
    "instruction" / Switch(lambda ctx: ctx.discriminant, {
        SplTokenInstructionDiscriminant.INITIALIZE_ACCOUNT: InitializeAccountInstruction,
        SplTokenInstructionDiscriminant.INITIALIZE_ACCOUNT2: InitializeAccount2Instruction,
        SplTokenInstructionDiscriminant.INITIALIZE_ACCOUNT3: InitializeAccount3Instruction,
        SplTokenInstructionDiscriminant.TRANSFER: TransferInstruction,
        SplTokenInstructionDiscriminant.TRANSFER_CHECKED: TransferCheckedInstruction,
    })
)
