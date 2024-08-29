__all__ = ['Pubkey', 'String', 'Option', 'Vec', 'StringWithLength', 'PaddedVecWithLength', 'PaddedOption']

from construct import (
    Struct, ExprAdapter, PrefixedArray, GreedyBytes,
    Prefixed, Array, Byte, Bytes,
    Int32ul, Int8ul, Padded,
    If, this,
)
from solders.pubkey import Pubkey as SoldersPubkey

Pubkey = ExprAdapter(
    Array(32, Byte),
    encoder=lambda obj, ctx: bytes(obj),
    decoder=lambda obj, ctx: SoldersPubkey(obj),
)

String = ExprAdapter(
    Prefixed(Int32ul, GreedyBytes),
    encoder=lambda obj, ctx: obj.encode('utf-8'),
    decoder=lambda obj, ctx: obj.decode('utf-8'),
)

StringWithLength = lambda length: ExprAdapter(
    Prefixed(Int32ul, Bytes(length)),
    encoder=lambda obj, ctx: obj.encode('utf-8'),
    decoder=lambda obj, ctx: obj.decode('utf-8'),
)

Option = lambda struct: ExprAdapter(
    Struct(
        "is_some" / Int8ul,
        "value" / If(this.is_some == 1, struct)
    ),
    encoder=lambda obj, ctx: {'is_some': 1 if obj else 0, 'value': obj},
    decoder=lambda obj, ctx: obj['value'] if obj['is_some'] == 1 else None,
)

PaddedOption = lambda struct: Padded(Int8ul.sizeof() + struct.sizeof(), Option(struct))

Vec = lambda struct: PrefixedArray(Int32ul, struct)

PaddedVecWithLength = lambda struct, length: Padded(Int32ul.sizeof() + struct.sizeof() * length, Vec(struct))

def get_field_offset(struct: Struct, field: str):
    offset = 0
    for subcon in struct.subcons:
        if subcon.name == field:
            return offset
        else:
            offset += subcon.sizeof()
    raise ValueError(f"'{struct.name}' has no field '{field}'")
