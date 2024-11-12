import numpy as np
def load_transactions(path_to_data, order):
    transactions = []
    with open(path_to_data, 'r') as fid:
        for lines in fid:
            str_line = list(lines.strip().split(','))
            _t = list(np.unique(str_line))
            _t.sort(key=lambda x: order.index(x)) 
            transactions.append(_t)
    return transactions