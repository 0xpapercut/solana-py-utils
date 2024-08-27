import json
from dataclasses import dataclass

from solders.transaction_status import EncodedConfirmedTransactionWithStatusMeta
from solders.instruction import CompiledInstruction
from solders.pubkey import Pubkey

from .transaction import (
    get_transaction,
    get_meta,
    get_account_keys,
)

@dataclass
class StructuredInstruction:
    program_id: Pubkey
    accounts: list[Pubkey]
    stack_height: int
    data: str
    parent_instruction: 'StructuredInstruction'
    inner_instructions: list['StructuredInstruction']

    @classmethod
    def _build_dangling_instruction(cls, instruction: CompiledInstruction, account_keys: list[Pubkey]) -> 'StructuredInstruction':
        instruction_json = json.loads(instruction.to_json())
        return cls(
            program_id=account_keys[instruction_json['programIdIndex']],
            accounts=[account_keys[index] for index in instruction_json['accounts']],
            data=instruction_json['data'],
            stack_height=instruction_json['stackHeight'] or 1,
            parent_instruction=None,
            inner_instructions=[]
        )

    @classmethod
    def build_structured_instructions(cls, confirmed_transaction: EncodedConfirmedTransactionWithStatusMeta) -> list['StructuredInstruction']:
        account_keys = get_account_keys(confirmed_transaction)
        flattened_instructions = [cls._build_dangling_instruction(instruction, account_keys) for instruction in flattened_compiled_instructions(confirmed_transaction)]
        structured_instructions: list[StructuredInstruction] = []
        instruction_stack: list[StructuredInstruction] = []

        while flattened_instructions:
            popped_instruction = flattened_instructions.pop(0)
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

        return structured_instructions

@dataclass
class StructuredInstructions:
    instructions: list['StructuredInstruction']

    @classmethod
    def build(cls, confirmed_transaction: EncodedConfirmedTransactionWithStatusMeta):
        account_keys = get_account_keys(confirmed_transaction)
        flattened_instructions = [StructuredInstruction._build_dangling_instruction(instruction, account_keys) for instruction in flattened_compiled_instructions(confirmed_transaction)]
        structured_instructions: list[StructuredInstruction] = []
        instruction_stack: list[StructuredInstruction] = []

        while flattened_instructions:
            popped_instruction = flattened_instructions.pop(0)
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

def flattened_compiled_instructions(confirmed_transaction: EncodedConfirmedTransactionWithStatusMeta) -> list[CompiledInstruction]:
    flattened = []

    main_instructions = get_main_instructions(confirmed_transaction)
    inner_instructions = get_inner_instructions(confirmed_transaction)

    inner_instructions_index = 0
    for i, instruction in enumerate(main_instructions):
        flattened.append(instruction)
        if inner_instructions_index < len(inner_instructions) and i == inner_instructions[inner_instructions_index].index:
            flattened.extend(inner_instructions[inner_instructions_index].instructions)
            inner_instructions_index += 1

    return flattened

def get_main_instructions(confirmed_transaction: EncodedConfirmedTransactionWithStatusMeta) -> list[CompiledInstruction]:
    return get_transaction(confirmed_transaction).message.instructions

def get_inner_instructions(confirmed_transaction: EncodedConfirmedTransactionWithStatusMeta):
    return get_meta(confirmed_transaction).inner_instructions
