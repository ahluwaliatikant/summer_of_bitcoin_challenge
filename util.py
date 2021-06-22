import csv


def read_data(filename):
    """
    Read csv file to create a list of all transactions
    """
    transactions = []

    with open(filename, 'r') as infile:
        reader = csv.reader(infile, delimiter=',')
        header_read = False
        for line in reader:
            if not header_read:
                header_read = True
                continue
            txn = dict()
            txn['txid'] = line[0]
            txn['fee'] = int(line[1])
            txn['weight'] = int(line[2])
            txn['parents'] = line[3].split(';') if line[3] != '' else []
            transactions.append(txn)

    return transactions


def write_to_file(transaction_ids, filename):
    with open(filename, 'w') as outfile:
        for tx_id in transaction_ids:
            outfile.write(f'{tx_id}\n')
    return


def topological_sort(transactions, index, visited, stack):
    visited[index] = True

    for transaction_id in transactions[index].children:
        transaction_index = [t.txid for t in transactions].index(transaction_id)
        if not visited[transaction_index]:
            topological_sort(transactions, transaction_index, visited, stack)

    stack.append(transactions[index])


def generate_topological_sorted_list(transactions):
    """
    Create a list containing transactions in topologically sorted order.
    Each transaction appears only after all it's parents
    """
    total_txns = len(transactions)
    stack = []
    visited = [False]*total_txns

    for i in range(total_txns):
        if not visited[i]:
            topological_sort(transactions, i, visited, stack)

    return stack
