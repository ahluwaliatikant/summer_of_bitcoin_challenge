from transaction import TransactionSetPriorityQueue
from util import read_data, write_to_file
from settings import MAX_WEIGHT, INPUT_FILE, OUTPUT_FILE


def get_mined_transactions_using_greedy_priority(txns, comparator_method):
    """
    Approach 1 (Greedy):
    Keep a set of possible choices of transactions miner can pick from.
    Choose the one with the highest priority. Include it in the mined transactions
    If any of it's children has all parents included
        add it to set of valid choices.
    """

    txn_set = TransactionSetPriorityQueue(txns, comparator_method)
    mined_txns = list()
    mined_weight = 0
    total_fee = 0

    while not txn_set.is_empty():
        mined_txn = txn_set.release_transaction()
        if mined_weight + mined_txn.weight >= MAX_WEIGHT:
            break

        mined_txns.append(mined_txn.txid)
        mined_weight = mined_weight + mined_txn.weight
        total_fee = total_fee + mined_txn.fee

    result = {
        'fee': total_fee,
        'weight': mined_weight,
        'mined_transactions': mined_txns
    }
    return result


def get_mined_transactions_greedy():
    """
    Main Method to Get Max Fee using Greedy Paradigm
    """
    transactions = read_data(INPUT_FILE)

    # Get max fee using 3 priority setting factors:
    # 1. Max Fee/Weight Ratio
    # 2. Max Fee
    # 3. Max Weight

    result_using_fee_by_weight_priority = get_mined_transactions_using_greedy_priority(transactions, 'fee_by_weight')
    result_using_weight_priority = get_mined_transactions_using_greedy_priority(transactions, 'weight')
    result_using_fee_priority = get_mined_transactions_using_greedy_priority(transactions, 'fee')

    mined_weight, fee_collected, mined_transactions = 0, 0, list()

    if result_using_fee_by_weight_priority['fee'] > fee_collected:
        fee_collected = result_using_fee_by_weight_priority['fee']
        mined_weight = result_using_fee_by_weight_priority['weight']
        mined_transactions = result_using_fee_by_weight_priority['mined_transactions']

    if result_using_fee_priority['fee'] > fee_collected:
        fee_collected = result_using_fee_priority['fee']
        mined_weight = result_using_fee_priority['weight']
        mined_transactions = result_using_fee_priority['mined_transactions']

    if result_using_weight_priority['fee'] > fee_collected:
        fee_collected = result_using_weight_priority['fee']
        mined_weight = result_using_weight_priority['weight']
        mined_transactions = result_using_weight_priority['mined_transactions']

    print(f'Fee Collected: {fee_collected}, Weight of Block: {mined_weight}')

    return mined_transactions

