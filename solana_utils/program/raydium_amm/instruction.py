from enum import IntEnum
from construct import (
    Int8ul,
    Int16ul,
    Int64ul,
    Struct,
    Switch,
    Pass,
)
from ...construct import Pubkey

InitializeInstruction = Struct(
    "nonce" / Int8ul,
    "open_time" / Int64ul,
)

InitializeInstruction2 = Struct(
    "nonce" / Int8ul,
    "open_time" / Int64ul,
    "init_pc_amount" / Int64ul,
    "init_coin_amount" / Int64ul,
)

PreInitializeInstruction = Struct(
    "nonce" / Int8ul,
)

MonitorStepInstruction = Struct(
    "plan_order_limit" / Int16ul,
    "place_order_limit" / Int16ul,
    "cancel_order_limit" / Int16ul,
    "base_side" / Int64ul,
)

DepositInstruction = Struct(
    "max_coin_amount" / Int64ul,
    "max_pc_amount" / Int64ul,
    "base_side" / Int64ul,
)

WithdrawInstruction = Struct(
    "amount" / Int64ul,
)

SetParamsInstruction = Struct(
    "param" / Int8ul,
    "value" / Int64ul,
    "new_pubkey" / Pubkey,
    "fees" / Int64ul,
    "last_order_distance" / Int64ul,
)

WithdrawSrmInstruction = Struct(
    "amount" / Int64ul,
)

SwapInstructionBaseIn = Struct(
    "amount_in" / Int64ul,
    "minimum_amount_out" / Int64ul,
)

SwapInstructionBaseOut = Struct(
    "max_amount_in" / Int64ul,
    "amount_out" / Int64ul,
)

SimulateInstruction = Struct(
    "param" / Int8ul,
    "swap_base_in_value" / SwapInstructionBaseIn,
    "swap_base_out_value" / SwapInstructionBaseOut,
)

AdminCancelOrdersInstruction = Struct(
    "limit" / Int16ul,
)

ConfigArgs = Struct(
    "param" / Int8ul,
    "owner" / Pubkey,
    "create_pool_fee" / Int64ul,
)

MigrateToOpenBook = Struct()
WithdrawPnl = Struct()
CreateConfigAccount = Struct()


class RaydiumAmmDiscriminant(IntEnum):
    INITIALIZE = 0
    INITIALIZE2 = 1
    MONITOR_STEP = 2
    DEPOSIT = 3
    WITHDRAW = 4
    MIGRATE_TO_OPENBOOK = 5
    SET_PARAMS = 6
    WITHDRAW_PNL = 7
    WITHDRAW_SRM = 8
    SWAP_BASE_IN = 9
    PRE_INITIALIZE = 10
    SWAP_BASE_OUT = 11
    SIMULATE = 12
    ADMIN_CANCEL_ORDERS = 13
    CREATE_CONFIG_ACCOUNT = 14
    UPDATE_CONFIG_ACCOUNT = 15

RaydiumAmmInstruction = Struct(
    "discriminant" / Int8ul,
    "instruction" / Switch(lambda ctx: ctx.discriminant, {
        RaydiumAmmDiscriminant.INITIALIZE: InitializeInstruction,
        RaydiumAmmDiscriminant.INITIALIZE2: InitializeInstruction2,
        RaydiumAmmDiscriminant.MONITOR_STEP: MonitorStepInstruction,
        RaydiumAmmDiscriminant.DEPOSIT: DepositInstruction,
        RaydiumAmmDiscriminant.WITHDRAW: WithdrawInstruction,
        RaydiumAmmDiscriminant.MIGRATE_TO_OPENBOOK: MigrateToOpenBook,
        RaydiumAmmDiscriminant.SET_PARAMS: SetParamsInstruction,
        RaydiumAmmDiscriminant.WITHDRAW_PNL: WithdrawPnl,
        RaydiumAmmDiscriminant.WITHDRAW_SRM: WithdrawSrmInstruction,
        RaydiumAmmDiscriminant.SWAP_BASE_IN: SwapInstructionBaseIn,
        RaydiumAmmDiscriminant.PRE_INITIALIZE: PreInitializeInstruction,
        RaydiumAmmDiscriminant.SWAP_BASE_OUT: SwapInstructionBaseOut,
        RaydiumAmmDiscriminant.SIMULATE: SimulateInstruction,
        RaydiumAmmDiscriminant.ADMIN_CANCEL_ORDERS: AdminCancelOrdersInstruction,
        RaydiumAmmDiscriminant.CREATE_CONFIG_ACCOUNT: CreateConfigAccount,
        RaydiumAmmDiscriminant.UPDATE_CONFIG_ACCOUNT: Pass,
    })
)
