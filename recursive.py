from transaction import TransactionSetNoPriority
from util import read_data, generate_topological_sorted_list, write_to_file
from settings import MAX_WEIGHT, INPUT_FILE, OUTPUT_FILE

# Overriding python's default recursion limit
import sys
sys.setrecursionlimit(6000)

mine_transaction_dp_cache = dict()


def mine_transaction(topologically_sorted_transactions, index, curr_weight, curr_fee, curr_mined_transactions):
    """
    Approach 2: Recursive ( If number of transactions is less)
    Greedy would not be able to give max fee possible in all cases.
    To optimize result, we use recursive with time as tradeoff.
    """

    if index < 0:
        return curr_fee, curr_mined_transactions

    # Choose to skip this transaction
    max_fee, mined_transactions = 0, []
    fee_1, mined_transactions_1 = mine_transaction(topologically_sorted_transactions, index-1, curr_weight, curr_fee, curr_mined_transactions)

    fee_2, mined_transactions_2 = 0, []
    curr_txn = topologically_sorted_transactions[index]
    if len(curr_txn.parents) == 0 and curr_txn.weight + curr_weight <= MAX_WEIGHT:
        # Choose to include this transaction
        for child_id in curr_txn.children:
            for txn in topologically_sorted_transactions:
                if txn.txid == child_id:
                    txn.parents.remove(curr_txn.txid)
        fee_2, mined_transactions_2 = mine_transaction(topologically_sorted_transactions, index-1, curr_weight+curr_txn.weight, curr_fee+curr_txn.fee, curr_mined_transactions + [curr_txn])

        for child_id in curr_txn.children:
            for txn in topologically_sorted_transactions:
                if txn.txid == child_id:
                    txn.parents.append(curr_txn.txid)

    if fee_1 > max_fee:
        max_fee = fee_1
        mined_transactions = mined_transactions_1

    if fee_2 > max_fee:
        max_fee = fee_2
        mined_transactions = mined_transactions_2

    return max_fee, mined_transactions


def mine_transaction_with_dp_cache(topologically_sorted_transactions, index, curr_weight, curr_fee, curr_mined_transactions):
    """
    Approach 3: Recursive With DP Cache ( If number of transactions is less)
    To optimize time, we store results for some recursive calls.
    """

    global mine_transaction_dp_cache

    if index < 0:
        return curr_fee, curr_mined_transactions

    is_eligible = len(topologically_sorted_transactions[index].parents) == 0
    stored_ans = mine_transaction_dp_cache.get(f'{index},{curr_weight},{is_eligible}', None)
    if stored_ans is not None:
        return stored_ans[0], stored_ans[1]

    # Choose to skip this transaction
    max_fee, mined_transactions = 0, []
    fee_1, mined_transactions_1 = mine_transaction_with_dp_cache(topologically_sorted_transactions, index-1, curr_weight, curr_fee, curr_mined_transactions)

    fee_2, mined_transactions_2 = 0, []
    curr_txn = topologically_sorted_transactions[index]
    if len(curr_txn.parents) == 0 and curr_txn.weight + curr_weight <= MAX_WEIGHT:
        # Choose to include this transaction
        for child_id in curr_txn.children:
            for txn in topologically_sorted_transactions:
                if txn.txid == child_id:
                    txn.parents.remove(curr_txn.txid)
        fee_2, mined_transactions_2 = mine_transaction_with_dp_cache(topologically_sorted_transactions, index-1, curr_weight+curr_txn.weight, curr_fee+curr_txn.fee, curr_mined_transactions + [curr_txn])

        for child_id in curr_txn.children:
            for txn in topologically_sorted_transactions:
                if txn.txid == child_id:
                    txn.parents.append(curr_txn.txid)

    if fee_1 > max_fee:
        max_fee = fee_1
        mined_transactions = mined_transactions_1

    if fee_2 > max_fee:
        max_fee = fee_2
        mined_transactions = mined_transactions_2

    mine_transaction_dp_cache[f'{index},{curr_weight},{is_eligible}'] = [max_fee, mined_transactions]
    return max_fee, mined_transactions


def get_mined_transactions_recursive_without_cache():
    txns = read_data(INPUT_FILE)

    txn_set = TransactionSetNoPriority(txns)

    # Generate topologically sorted order of transactions
    topologically_sorted_transactions = generate_topological_sorted_list(list(txn_set.all_txns.values()))

    fee_collected, mined_transactions = mine_transaction(topologically_sorted_transactions, len(topologically_sorted_transactions)-1, 0, 0, [])

    print(f'Fee Collected: {fee_collected}')

    # Writing mined transactions to block.txt file
    write_to_file([t.txid for t in mined_transactions], OUTPUT_FILE)

    return


def get_mined_transactions_recursive_with_cache():
    txns = read_data(INPUT_FILE)

    txn_set = TransactionSetNoPriority(txns)

    # Generate topologically sorted order of transactions
    topologically_sorted_transactions = generate_topological_sorted_list(list(txn_set.all_txns.values()))

    fee_collected, mined_transactions = mine_transaction_with_dp_cache(topologically_sorted_transactions, len(topologically_sorted_transactions)-1, 0, 0, [])

    print(f'Fee Collected: {fee_collected}')

    # Writing mined transactions to block.txt file
    write_to_file([t.txid for t in mined_transactions], OUTPUT_FILE)

    return
