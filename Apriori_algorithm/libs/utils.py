import numpy as np


def load_transactions(path_to_data, order):
    transactions = []
    with open(path_to_data, 'r') as fid:
        for lines in fid:
            str_line = [item.strip() for item in lines.strip().split(',')]
            _t = list(np.unique(str_line))
            _t.sort(key=lambda x: order.index(x)) 
            transactions.append(_t)
    return transactions

def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

def join_two_itemsets(it1, it2, order):
    it1.sort(key=lambda x: order.index(x))
    it1.sort(key=lambda x: order.index(x))

    for i in range(len(it1) - 1):
        if it1[i] != it2[i]:
            return []
        
    return it1 + [it2[-1]]
    

def join_set_itemsets(set_of_items, order):
    C = []
    for i in range(len(set_of_items)):
        for j in range(i + 1, len(set_of_items)):
            it_out = join_two_itemsets(set_of_items[i], set_of_items[j], order)
            if len(it_out) > 0:
                C.append(it_out)
    return C 

def count_occurences(itemset, transactions):
    count = 0 
    for i in range(len(transactions)):
        if set(itemset).issubset(set(transactions[i])):
            count += 1
    return count

def get_frequent(itemsets, transactions, min_support, prev_discarded):
    L = []
    supp_count = []
    new_discarded = []

    k = len(prev_discarded.keys())

    for s in range(len(itemsets)):
        discarded_before = False
        if k > 0:
            for it in prev_discarded[k]:
                if set(it).issubset(set(itemsets[s])):
                    discarded_before = True
                    break

        if not discarded_before:
            count = count_occurences(itemsets[s], transactions)
            if count/len(transactions) >= min_support:
                L.append(itemsets[s]) 
                supp_count.append(count)
            else:
                new_discarded.append(itemsets[s])

    return L, supp_count, new_discarded   

def powerset(s):
    rules = []
    for r in range(1, len(s)):
       rule = combinations(s,r)
       rules += rule 
        
    return list(rules)

#printing out the rules
def write_rules(X, X_S, S, conf, supp, lift, num_trans):
    out_rules = ""
    out_rules += "Freq. Itemset: {}\n".format(X)
    out_rules += "    Rule: {} -> {} \n".format(list(S), list(X_S))
    out_rules += "    Conf: {0:2.3f} ".format(conf)
    out_rules += "    Supp: {0:2.3f} ".format(supp / num_trans)
    out_rules += "    Lift: {0:2.3f} \n".format(lift)
    return out_rules 

def print_table(T, supp_count):
        print("Itemset | Frequency")
        for k in range(len(T)):
            print("{}  :  {}".format(T[k], supp_count[k]))
        print("\n")
