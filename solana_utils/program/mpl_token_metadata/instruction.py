from enum import IntEnum
from construct import (
    Struct,
    Switch,
    Int8ul,
)
from ...construct import *
from .state import DataV2, CollectionDetails

class MplTokenMetadataInstructionDiscriminant(IntEnum):
    CREATE_METADATA_ACCOUNT_V3 = 33
    # TODO

CreateMetadataAccountV3Instruction = Struct(
    "data" / DataV2,
    "is_mutable" / Int8ul,
    "collection_details" / Option(CollectionDetails)
)

MplTokenMetadataInstruction = Struct(
    "discriminant" / Int8ul,
    "instruction" / Switch(lambda ctx: ctx.discriminant, {
        MplTokenMetadataInstructionDiscriminant.CREATE_METADATA_ACCOUNT_V3: CreateMetadataAccountV3Instruction,
    })
)
