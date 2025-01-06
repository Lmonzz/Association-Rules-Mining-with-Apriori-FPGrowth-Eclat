import numpy as np
from collections import defaultdict

def load_order(path_to_order):
    order = []
    with open(path_to_order, 'r') as fid:
        for lines in fid:
            str_line = lines.strip()
            order.append(str_line)
        order = sorted(order)
    return order

def load_transactions(path_to_data, order):
    transactions = []
    with open(path_to_data, 'r') as fid:
        for lines in fid:
            str_line = [item.strip() for item in lines.strip().split(',')]
            t = list(np.unique(str_line))
            t.sort(key=lambda x: order.index(x)) 
            transactions.append(t)
    return transactions

def eclat(C, minsup):
    for i, (X, tX) in enumerate(C): 
        if len(tX) >= minsup:  
            print(f"Frequent itemset: {set(X)}, support: {len(tX)}")
        T = []  
        for j in range(i + 1, len(C)):  
            Y, tY = C[j]
            R = X | Y  
            tR = tX & tY  
            if len(tR) >= minsup: 
                T.append((R, tR)) 
        if T:
            eclat(T, minsup) 

def preprocess_dataset(dataset, minsup):
    C1 = defaultdict(set)
    for tid, transaction in enumerate(dataset): 
        for item in transaction:
            C1[frozenset([item])].add(tid)
    return sorted(
        [(itemset, tidset) for itemset, tidset in C1.items() if len(tidset) >= minsup],
        key=lambda x: len(x[1])
    )

