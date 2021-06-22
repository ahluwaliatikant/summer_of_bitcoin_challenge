"""
Main File to Generate Mined Transactions Using Different Approaches
"""
from greedy import get_mined_transactions_greedy
from recursive import get_mined_transactions_recursive_without_cache, get_mined_transactions_recursive_with_cache
from util import write_to_file
from settings import OUTPUT_FILE


def mine_transactions_from_mempool():
    approach_used = 1
    mined_transactions = None

    if approach_used == 1:
        mined_transactions = get_mined_transactions_greedy()

    if approach_used == 2:
        mined_transactions = get_mined_transactions_recursive_without_cache()

    if approach_used == 3:
        mined_transactions = get_mined_transactions_recursive_with_cache()

    if mined_transactions is None:
        print('Error in mining transactions')
        return

    # Writing mined transactions to block.txt file
    write_to_file(mined_transactions, OUTPUT_FILE)
    return


mine_transactions_from_mempool()
