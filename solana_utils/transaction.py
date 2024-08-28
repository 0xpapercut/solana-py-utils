from solders.transaction_status import EncodedConfirmedTransactionWithStatusMeta, EncodedTransactionWithStatusMeta

def get_encoded_transaction_with_status_meta(transaction) -> EncodedTransactionWithStatusMeta:
    if isinstance(transaction, EncodedTransactionWithStatusMeta):
        return transaction
    elif isinstance(transaction, EncodedConfirmedTransactionWithStatusMeta):
        return transaction.transaction

def get_message(transaction):
    return get_encoded_transaction_with_status_meta(transaction).transaction.message

def get_meta(transaction):
    return get_encoded_transaction_with_status_meta(transaction).meta

def get_account_keys(transaction):
    meta = get_meta(transaction)
    message = get_message(transaction)

    return message.account_keys + meta.loaded_addresses.writable + meta.loaded_addresses.readonly

def get_signature(transaction):
    return get_encoded_transaction_with_status_meta(transaction).transaction.signatures[0]

def get_signers(transaction):
    num_required_signatures = get_message(transaction).header.num_required_signatures
    return get_account_keys(transaction)[:num_required_signatures]
