import numpy as np

# trang 38 mục 5.6 thuật toán FP-Growth 
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

# Tree Node class
class TreeNode:
    def __init__(self, item, count, parent):
        self.item = item       
        self.count = count     
        self.parent = parent   
        self.children = {}     
        self.link = None       

def count_item_frequencies(transactions):
    item_counts = {}
    for transaction in transactions:
        for item in transaction:
            if item in item_counts:
                item_counts[item] += 1
            else:
                item_counts[item] = 1
    return item_counts

def sort_items(items, item_counts):
    return sorted(items, key=lambda x: item_counts[x], reverse=True)


# FP-Tree construction
def build_fp_tree(transactions, min_support):
    # Step 1: đếm support của item
    item_counts = count_item_frequencies(transactions)
    # Remove items below min_support
    for item in list(item_counts.keys()):
        if item_counts[item] < min_support:
            del item_counts[item]
    if len(item_counts) == 0:
        return None, None 
    # Step 2: tạo tree root với header_table
    root = TreeNode(None, 0, None)
    header_table = {}
    # Step 3: thêm các tập giao dịch đc sắp xếp vào fp-trê
    for transaction in transactions:
        # lọc và sắp xếp items
        filtered_items = [item for item in transaction if item in item_counts]
        sort_items(filtered_items, item_counts)  
        # chèn giao dịch vào tree
        current_node = root
        for item in filtered_items:
            if item in current_node.children:
                current_node.children[item].count += 1
            else:
                new_node = TreeNode(item, 1, current_node)
                current_node.children[item] = new_node
                # cập nhập header_table
                if item not in header_table:
                    header_table[item] = new_node
                else:
                    # Link node mới tới nodes đã tồn tại trong header table
                    temp = header_table[item]
                    while temp.link is not None:
                        temp = temp.link
                    temp.link = new_node
            current_node = current_node.children[item]  
    return root, header_table

# tìm conditional patterns cho 1 item
def find_conditional_patterns(header_table, item):
    node = header_table[item]
    patterns = []
    while node:
        path = []
        parent = node.parent
        while parent and parent.item is not None:
            path.append(parent.item)
            parent = parent.parent
        if path:
            for _ in range(node.count):
                patterns.append(path[::-1])  
        node = node.link
    return patterns

# đệ quy FP-Growth mining
def fp_growth(header_table, min_support, prefix, frequent_itemsets):
    for item in header_table:
        # tạo frequent itemset
        new_prefix = prefix + [item]
        total_support = 0
        node = header_table[item]
        while node:
            total_support += node.count
            node = node.link
        frequent_itemsets.append((new_prefix, total_support))
        
        # tìm conditional patterns
        conditional_patterns = find_conditional_patterns(header_table, item)
        if not conditional_patterns:
            continue
        
        # dựng conditional FP-tree
        conditional_root, conditional_header = build_fp_tree(conditional_patterns, min_support)
        if conditional_root:
            fp_growth(conditional_header, min_support, new_prefix, frequent_itemsets)


def run_fp_growth(transactions, min_support):
    root, header_table = build_fp_tree(transactions, min_support)
    if not root:
        print("No frequent itemsets found.")
        return []
    frequent_itemsets = []
    fp_growth(header_table, min_support, [], frequent_itemsets)
    return frequent_itemsets


