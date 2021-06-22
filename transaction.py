from settings import MAX_WEIGHT
from queue import PriorityQueue


def compare_txn_fee_by_weight(txn_1, txn_2):
    """
    Compare Transactions based on fee to weight ratio. Higher Ratio -> Higher Priority
    """
    return txn_1.fee/txn_1.weight > txn_2.fee/txn_2.weight


def compare_txn_fee(txn_1, txn_2):
    """
    Compare Transactions based on fee. Higher Fee -> Higher Priority
    """
    return txn_1.fee > txn_2.fee


def compare_txn_weight(txn_1, txn_2):
    """
    Compare Transactions based on weight. Lower wt -> Higher Priority
    """
    return txn_1.weight < txn_2.weight


COMPARATOR_FUNCTIONS = {
    'fee_by_weight': compare_txn_fee_by_weight,
    'fee': compare_txn_fee,
    'weight': compare_txn_weight
}


class Transaction:
    """
    Holds all properties of a transaction in mempool.
    """
    def __init__(self, txid, fee, weight, cmp_method, parent_txids=None):
        self.txid = txid
        self.fee = fee
        self.weight = weight
        self.cmp_method = cmp_method
        self.available = True
        self.parents = parent_txids if parent_txids is not None else list()  # List of parent TXIDs
        self.children = list()  # List of children TXIDs

    def __lt__(self, other):
        """
        Defines how to compare two transaction objects for priority setting
        """
        return self.cmp_method(self, other)


class TransactionSet:
    """
    Interface for any Transaction Set
    """
    def __init__(self, txns):
        self.txns = txns if txns is not None else list()

    def insert_transaction(self, txn):
        pass

    def release_transaction(self):
        pass

    def generate_txn_set(self):
        pass


class TransactionSetPriorityQueue(TransactionSet):
    """
    Transaction Set that uses Priority Queue to maintain available choices
    """
    def __init__(self, txns, comparator_method='fee_by_weight'):
        super().__init__(txns)
        self.all_txns = dict()
        self.txn_pq = PriorityQueue()
        self.comparator_method = COMPARATOR_FUNCTIONS[comparator_method]
        self.generate_txn_set()

    def create_txn(self, txn):
        return Transaction(txn['txid'], txn['fee'], txn['weight'], self.comparator_method, txn['parents'])

    def add_to_pq(self, txn):
        """
        Add transaction object to PriorityQueue
        """
        self.txn_pq.put(txn)

    def generate_txn_set(self):
        """
        Initially add all transactions with NO Parents to Priority Queue.
        Populate Children for every transaction in the set.
        """
        for txn in self.txns:
            t = self.create_txn(txn)
            self.all_txns[t.txid] = t
            if len(t.parents) == 0 and t.weight <= MAX_WEIGHT:
                self.add_to_pq(t)
                t.available = False

        for txid, txn in self.all_txns.items():
            for pid in txn.parents:
                parent = self.all_txns[pid]
                parent.children.append(txid)

    def insert_transaction(self, txn):
        """
        Insert transaction to the Priority Queue
        """
        t = self.create_txn(txn)
        self.add_to_pq(t)

    def release_transaction(self):
        """
        Return the highest priority transaction from Queue.
        Add all children to priority queue whose all parents have been picked
        """
        t = self.txn_pq.get()
        for child_id in t.children:
            child = self.all_txns[child_id]
            child.parents.remove(t.txid)
            if len(child.parents) == 0 and t.available:
                self.add_to_pq(self.all_txns[child_id])
                t.available = False
        return t

    def is_empty(self):
        """
        Return if the PriorityQueue is empty or not
        """
        return self.txn_pq.empty()


class TransactionSetNoPriority(TransactionSet):
    """
    Transaction Set without Priority Queue
    """
    def __init__(self, txns):
        super().__init__(txns)
        self.all_txns = dict()
        self.generate_txn_set()

    def create_txn(self, txn):
        return Transaction(txn['txid'], txn['fee'], txn['weight'], compare_txn_fee_by_weight, txn['parents'])

    def generate_txn_set(self):
        """
        Create transaction objects for all transactions.
        Populate chidlren for each trnasaction
        """
        for txn in self.txns:
            t = self.create_txn(txn)
            self.all_txns[t.txid] = t

        for txid, txn in self.all_txns.items():
            for pid in txn.parents:
                parent = self.all_txns[pid]
                parent.children.append(txid)
