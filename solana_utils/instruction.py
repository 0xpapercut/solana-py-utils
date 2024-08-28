import json
import base64
import base58
from dataclasses import dataclass

from solders.transaction_status import EncodedConfirmedTransactionWithStatusMeta
from solders.instruction import CompiledInstruction
from solders.pubkey import Pubkey

from .transaction import get_message, get_meta, get_account_keys
from .token import TokenAccount
from .program.spl_token.constants import TOKEN_PROGRAM_ID
from .program.spl_token.instruction import SplTokenInstruction, SplTokenInstructionDiscriminant

@dataclass
class InstructionContext:
    token_accounts: dict[Pubkey, TokenAccount]

    @classmethod
    def partial_build(cls, transaction: EncodedConfirmedTransactionWithStatusMeta):
        meta = get_meta(transaction)
        account_keys = get_account_keys(transaction)
        token_accounts: dict[Pubkey, TokenAccount] = {}
        for token_balance in meta.pre_token_balances:
            token_account = TokenAccount.from_token_balance(token_balance, account_keys)
            token_accounts[token_account.address] = token_account

        return cls(token_accounts=token_accounts)

    def update(self, instruction: 'StructuredInstruction'):
        if instruction.program_id == TOKEN_PROGRAM_ID:
            decoded = SplTokenInstruction.parse(instruction.data)
            match decoded.discriminant:
                case SplTokenInstructionDiscriminant.INITIALIZE_ACCOUNT:
                    address = instruction.accounts[0]
                    mint = instruction.accounts[1]
                    owner = instruction.accounts[2]
                    self.token_accounts[address] = TokenAccount(mint=mint, address=address, owner=owner)
                case (SplTokenInstructionDiscriminant.INITIALIZE_ACCOUNT2 | SplTokenInstructionDiscriminant.INITIALIZE_ACCOUNT3):
                    address = instruction.accounts[0]
                    mint = instruction.accounts[1]
                    owner = decoded.instruction.owner
                    self.token_accounts[address] = TokenAccount(mint=mint, address=address, owner=owner)

@dataclass
class StructuredInstruction:
    program_id: Pubkey
    accounts: list[Pubkey]
    stack_height: int
    data: bytes
    parent_instruction: 'StructuredInstruction'
    inner_instructions: list['StructuredInstruction']
    context: InstructionContext

    @classmethod
    def _build_dangling_instruction(cls, instruction: CompiledInstruction, account_keys: list[Pubkey], context: InstructionContext, data_encoding: str = "base58") -> 'StructuredInstruction':
        data = instruction.data
        if data_encoding == "base58":
            data = base58.b58decode(data)
        elif data_encoding == "base64":
            data = base64.b64decode(data)
        return cls(
            program_id=account_keys[instruction.program_id_index],
            accounts=[account_keys[index] for index in instruction.accounts],
            data=data,
            stack_height=json.loads(instruction.to_json()).get('stackHeight') or 1,
            parent_instruction=None,
            inner_instructions=[],
            context=context,
        )

@dataclass
class StructuredInstructions:
    instructions: list['StructuredInstruction']

    @classmethod
    def build(cls, transaction: EncodedConfirmedTransactionWithStatusMeta):
        account_keys = get_account_keys(transaction)
        context = InstructionContext.partial_build(transaction)
        flattened_instructions = [StructuredInstruction._build_dangling_instruction(instruction, account_keys, context) for instruction in flattened_compiled_instructions(transaction)]

        structured_instructions: list[StructuredInstruction] = []
        instruction_stack: list[StructuredInstruction] = []

        while flattened_instructions:
            popped_instruction = flattened_instructions.pop(0)
            context.update(popped_instruction)
            while instruction_stack and popped_instruction.stack_height <= instruction_stack[-1].stack_height:
                if len(instruction_stack) > 1:
                    instruction_stack.pop()
                else:
                    structured_instructions.append(instruction_stack.pop())
            if instruction_stack:
                popped_instruction.parent_instruction = instruction_stack[-1]
                instruction_stack[-1].inner_instructions.append(popped_instruction)
            instruction_stack.append(popped_instruction)
        if instruction_stack:
            structured_instructions.append(instruction_stack.pop(0))

        return cls(instructions=structured_instructions)

    def flattened(self) -> list['StructuredInstruction']:
        flattened_instructions: list['StructuredInstruction'] = []

        instruction_stack: list['StructuredInstruction'] = []
        instruction_stack.extend(reversed(self.instructions))
        while instruction_stack:
            popped_instruction = instruction_stack.pop()
            flattened_instructions.append(popped_instruction)
            instruction_stack.extend(reversed(popped_instruction.inner_instructions))

        return flattened_instructions

def flattened_compiled_instructions(transaction: EncodedConfirmedTransactionWithStatusMeta) -> list[CompiledInstruction]:
    flattened = []

    main_instructions = get_main_instructions(transaction)
    inner_instructions = get_inner_instructions(transaction)

    inner_instructions_index = 0
    for i, instruction in enumerate(main_instructions):
        flattened.append(instruction)
        if inner_instructions_index < len(inner_instructions) and i == inner_instructions[inner_instructions_index].index:
            flattened.extend(inner_instructions[inner_instructions_index].instructions)
            inner_instructions_index += 1

    return flattened

def get_main_instructions(transaction) -> list[CompiledInstruction]:
    return get_message(transaction).instructions

def get_inner_instructions(transaction):
    return get_meta(transaction).inner_instructions
