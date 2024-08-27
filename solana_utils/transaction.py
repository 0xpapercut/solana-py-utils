from solders.transaction_status import EncodedConfirmedTransactionWithStatusMeta

def get_meta(confirmed_transaction: EncodedConfirmedTransactionWithStatusMeta):
    return confirmed_transaction.transaction.meta

def get_transaction(confirmed_transaction: EncodedConfirmedTransactionWithStatusMeta):
    return confirmed_transaction.transaction.transaction

def get_account_keys(confirmed_transaction: EncodedConfirmedTransactionWithStatusMeta):
    transaction = get_transaction(confirmed_transaction)
    meta = get_meta(confirmed_transaction)

    return transaction.message.account_keys + meta.loaded_addresses.writable + meta.loaded_addresses.readonly
