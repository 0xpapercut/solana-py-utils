__all__ = ['Pubkey', 'String', 'Option', 'Vec']

from construct import (
    Construct, Struct, ExprAdapter, PrefixedArray, GreedyBytes, Prefixed, Array, Byte,
    Int32ul, Int8ul,
    If, this,
)
from solders.pubkey import Pubkey as SoldersPubkey

PUBKEY_LENGTH: 32

def _singleton(arg):
    x = arg()
    return x

@_singleton
class Pubkey(Construct):
    def _parse(self, stream, context, path):
        return SoldersPubkey(stream.read(32))

    def _build(self, obj, stream, context, path):
        if not isinstance(obj, SoldersPubkey):
            raise TypeError("Expected a solders.pubkey.Pubkey object")

    def _sizeof(self, context, path):
        return PUBKEY_LENGTH

# Pubkey = ExprAdapter(
#     Array(32, Byte),
#     encoder=lambda obj, ctx: bytes(obj),
#     decoder=lambda obj, ctx: SoldersPubkey(obj),
# )

String = ExprAdapter(
    Prefixed(Int32ul, GreedyBytes),
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

Vec = lambda struct: PrefixedArray(Int32ul, struct)

def get_field_offset(struct: Struct, field: str):
    offset = 0
    for subcon in struct.subcons:
        if subcon.name == field:
            return offset
        else:
            offset += subcon.sizeof()
    raise ValueError(f"'{struct.name}' has no field '{field}'")
