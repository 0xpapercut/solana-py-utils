from enum import IntEnum
from construct import (
    Int8ul,
    Int16ul,
    Int64ul,
    Struct,
    Switch,
    Pass,
    Int32ul,
    Prefixed,
    GreedyBytes,
    ExprAdapter,
    Adapter,
    If,
    this,
    PrefixedArray,
    Enum
)
from ...construct import *

Creator = Struct(
    "address" / Pubkey,
    "verified" / Int8ul,
    "share" / Int8ul,
)

Collection = Struct(
    "verified" / Int8ul,
    "key" / Pubkey
)

Uses = Struct(
    "use_method" / Int8ul,
    "remaining" / Int64ul,
    "total" / Int64ul,
)

DataV2 = Struct(
    "name" / String,
    "symbol" / String,
    "uri" / String,
    "seller_fee_basis_points" / Int16ul,
    "creators" / Option(Vec(Creator)),
    "collection" / Option(Collection),
    "uses" / Option(Uses),
)

Data = Struct(
    "name" / String,
    "symbol" / String,
    "uri" / String,
    "seller_fee_basis_points" / Int16ul,
    "creators" / Option(Vec(Creator)),
)

Key = Enum(
    Int8ul,
    UNITIALIZED=0,
    EDITION_V1=1,
    MASTER_EDITION_V1=2,
    RESERVATION_LIST_V1=3,
    METADATA_V1=4,
    RESERVATION_LIST_V2=5,
    MASTER_EDITION_V2=6,
    EDITION_MARKER=7,
    USE_AUTHORITY_RECORD=8,
    COLLECTION_AUTHORITY_RECORD=9,
    TOKEN_OWNED_ESCROW=10,
    TOKEN_RECORD=11,
    METADATA_DELEGATE=12,
    EDITION_MARKER_V2=13,
    HOLDER_DELEGATE=14,
)

TokenStandard = Enum(
    Int8ul,
    NON_FUNGIBLE=0,
    FUNGIBLE_ASSET=1,
    FUNGIBLE=2,
    NON_FUNGIBLE_EDITION=3,
    PROGRAMMABLE_NON_FUNGIBLE=4,
    PROGRAMMABLE_NON_FUNGIBLE_EDITION=5,
)

CollectionDetails = Struct(
    "type" / Int8ul,
    "data" / Switch(lambda ctx: ctx.type, {
        0: Struct("size" / Int64ul),
        1: Struct("padding" / Int64ul),
    })
)

ProgrammableConfig = Struct(
    "type" / Int8ul,
    "data" / Switch(lambda ctx: ctx.type, {
        0: Struct("rule_set" / Option(Pubkey)),
    })
)

Metadata = Struct(
    "key" / Key,
    "update_authority" / Pubkey,
    "mint" / Pubkey,
    "data" / Data,
    "primary_sale_happend" / Int8ul,
    "is_mutable" / Int8ul,
    "edition_nonce" / Option(Int8ul),
    "token_standard" / Option(TokenStandard),
    "collection" / Option(Collection),
    "uses" / Option(Uses),
    "collection_details" / Option(CollectionDetails),
    "programmable_config" / Option(ProgrammableConfig),
)
