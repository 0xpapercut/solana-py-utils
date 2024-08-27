"""
Websocket example of solana_utils usage.

Before running, setup the SOLANA_HTTP and SOLANA_WEBSOCKET as environment variables.
"""

import os
import asyncio
import pprint

from solana.rpc.async_api import AsyncClient
from solana.rpc.websocket_api import connect
from solana.rpc.commitment import Confirmed

from solders.rpc.responses import BlockNotificationResult
from solders.transaction_status import UiConfirmedBlock, EncodedTransactionWithStatusMeta

from solana_utils.instruction import StructuredInstructions
from solana_utils.transaction import get_signature

def parse_block(block: UiConfirmedBlock):
    for transaction in block.transactions:
        parse_transaction(transaction)

def parse_transaction(transaction: EncodedTransactionWithStatusMeta):
    print(f"Parsing transaction with signature {get_signature(transaction)}")
    instructions = StructuredInstructions.build(transaction)
    pprint.pprint(instructions)

async def main():
    async_client = AsyncClient(os.environ['SOLANA_HTTP'])
    async with connect(os.environ['SOLANA_WEBSOCKET'], max_size=100_000_000) as websocket:
        await websocket.block_subscribe(max_supported_transaction_version=0, commitment=Confirmed)
        subscription_response = await websocket.recv()
        subscription_id = subscription_response[0].result
        try:
            while True:
                response = await websocket.recv()
                block_notification_result: BlockNotificationResult = response[0].result
                parse_block(block_notification_result.value.block)

        except asyncio.CancelledError:
            await websocket.block_unsubscribe(subscription_id)

if __name__ == '__main__':
    asyncio.run(main())
