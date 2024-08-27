from construct import Construct
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
