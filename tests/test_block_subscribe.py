# import os
# import pytest
# import base58
# from pprint import pprint

# from solana_utils.instruction import (
#     StructuredInstruction,
#     StructuredInstructions,
#     flattened_compiled_instructions,
#     get_main_instructions,
#     get_inner_instructions,
# )

# from solders.signature import Signature
# from solders.pubkey import Pubkey
# from solders.transaction_status import EncodedConfirmedTransactionWithStatusMeta

# from solana.rpc.api import Client

# @pytest.fixture(scope="module")
# def client() -> Client:
#     return Client(os.environ['SOLANA_HTTP'])

# @pytest.fixture(scope="module")
# def sample_raydium_swap_confirmed_transaction(client: Client) -> EncodedConfirmedTransactionWithStatusMeta:
#     signature = Signature.from_string('2JvxmigRaVSszUdVhXBNhkLQh1sxDQeB7MKLKNsk1tShdMEPLTqEkr3dshAz5zrSopRrPZsbhkwtnqJT7dHnpgBY')
#     return client.get_transaction(signature, max_supported_transaction_version=0).value

# def test_flattened_instructions(sample_raydium_swap_confirmed_transaction):
#     flattened = flattened_compiled_instructions(sample_raydium_swap_confirmed_transaction)
#     assert(len(flattened) == 13)

# def test_structured_instructions(sample_raydium_swap_confirmed_transaction):
#     structured = StructuredInstructions.build(sample_raydium_swap_confirmed_transaction)
#     assert(len(structured.instructions) == 5)
#     flattened = structured.flattened()
#     assert(len(flattened) == 13)

#     from spl.token._layouts import (
#         InstructionType as SplTokenInstructionType,
#         INSTRUCTIONS_LAYOUT as SplTokenInstruction,
#     )

#     close_account_instruction = structured.instructions[4]
#     decoded_data = SplTokenInstruction.parse(close_account_instruction.data)
#     assert decoded_data.instruction_type == SplTokenInstructionType.CLOSE_ACCOUNT

#     from solana_utils.program.spl_token.instruction import SplTokenInstructionDiscriminant, SplTokenInstruction

#     transfer_instruction = structured.instructions[3].inner_instructions[0].inner_instructions[0]
#     decoded_data = SplTokenInstruction.parse(transfer_instruction.data)
#     assert decoded_data.discriminant in (SplTokenInstructionDiscriminant.TRANSFER, SplTokenInstructionDiscriminant.TRANSFER_CHECKED)

# """
# Websocket example of solana_utils usage.

# Before running, setup the SOLANA_HTTP and SOLANA_WEBSOCKET as environment variables.
# """

# import os
# import asyncio
# import pprint

# from solana.rpc.async_api import AsyncClient
# from solana.rpc.websocket_api import connect
# from solana.rpc.commitment import Confirmed, Processed

# from solders.rpc.responses import BlockNotificationResult
# from solders.transaction_status import UiConfirmedBlock, EncodedTransactionWithStatusMeta

# from solana_utils.instruction import StructuredInstructions
# from solana_utils.transaction import get_signature

# import time

# def parse_block(block: UiConfirmedBlock):
#     # print(block.block_time)
#     print(time.time() - block.block_time)
#     # for transaction in block.transactions:
#     #     parse_transaction(transaction)

# def parse_transaction(transaction: EncodedTransactionWithStatusMeta):
#     print(f"Parsing transaction with signature {get_signature(transaction)}")
#     instructions = StructuredInstructions.build(transaction)
#     pprint.pprint(instructions)

# async def block_subscribe_example():
#     async_client = AsyncClient(os.environ['SOLANA_HTTP'])
#     async with connect(os.environ['SOLANA_WEBSOCKET'], max_size=100_000_000) as websocket:
#         # await websocket.block_subscribe(max_supported_transaction_version=0, commitment=Confirmed)
#         # await websocket.logs_subscribe(commitment=Processed)
#         await websocket.slots_updates_subscribe()
#         subscription_response = await websocket.recv()
#         subscription_id = subscription_response[0].result

#         response = await websocket.recv()
# []        print(response[0])
#                 # block_notification_result: BlockNotificationResult = response[0].result
#                 # parse_block(block_notification_result.value.block)

#         except asyncio.CancelledError: ...
#             # await websocket.block_unsubscribe(subscription_id)
#             # await websocket.logs_unsubscribe(subscription_id)

# if __name__ == '__main__':
#     asyncio.run(slot_updates_subscribe_example())
