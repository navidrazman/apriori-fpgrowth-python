from dataclasses import dataclass # node class
from collections import defaultdict # constructiong FP-Tree , constructiong conditional FP-Tree
from collections import Counter # for count items
import itertools # for generating k+1

# ----------- node class --------------------------------
@dataclass
class node:
    
    name: any            # node name
    parrent: any         # Parrent name
    children: dict       # dict of children
    count: int  = 0      # count (support count)

    def inc(self, c=1):
        self.count = self.count + c
        
    def path(self):
        if self.parrent.parrent is None:
            return (self.name,)
        else:
            return self.parrent.path() + (self.name,)
    
# ---------- constructiong FP-Tree ----------------------
def fptree(order, sorted_transactions):
    
    root = node('root', None, {}, 0)
    header_table = defaultdict(list)
    
    def insert(parrent_node, items_list):
        
        m = len(items_list)
        
        if m == 0: return
        
        first , *remaining = items_list
        
        if first in parrent_node.children:
            
            parrent_node.children[first].inc()
            
        else:
            child_node = node(first, parrent_node, {}, 1)
            
            parrent_node.children[first] = child_node
            
            header_table[first].append(child_node)
            
        insert( parrent_node.children[first], remaining )
        
    
    for transaction in sorted_transactions:
        insert(root, transaction)
        
        # sord header table by less order
    header_table = {key:value for key,value in \
                    sorted(header_table.items(), key=lambda x:order[x[0]], reverse=True)}
    
    return root, header_table

# ---------- constructiong conditional FP-Tree ----------------------
def cfp_tree(order, new_trasactions):
    
    root = node('root', None, {}, 0)
    header_table = defaultdict(list)
    
    # ---------------------------------------------------
    def insert(parrent_node, items_list, count):
        
        m = len(items_list)
        
        if m == 0: return
        
        first , *remaining = items_list
        
        if first in parrent_node.children:
            
            parrent_node.children[first].inc(count)
            
        else:
            child_node = node(first, parrent_node, {}, count)
            
            parrent_node.children[first] = child_node
            
            header_table[first].append(child_node)
            
        insert( parrent_node.children[first], remaining, count)
    # ----------------------------------------------------- 
    
    for transaction,count in new_trasactions.items():
        
        insert(root, transaction, count)
        
    # sord header table by less order
    header_table = {key:value for key,value in \
                    sorted(header_table.items(), key=lambda x:order[x[0]], reverse=True)}
    
    return root, header_table

def conditional_fp(order, root, header_table, min_sup_count = 1):
    
    frequent_itemset = defaultdict(int)
    
    if root.children == {} :
        return []
    
    for item, linked_list in header_table.items():
        
        sup_count = sum ( ( nd.count for nd in linked_list ) )
        
        if sup_count < min_sup_count: # skip if sup count less the min_sup_count
            continue
            
        frequent_itemset[(item,)] = sup_count # add item if it's supp count >= min_sup_count
        
        # generate frequent_items
        new_trasactions = { node_in_list.path()[:-1]:node_in_list.count for node_in_list in linked_list}
        
        new_root, new_header_table = cfp_tree(order, new_trasactions)
        
        if new_root.children != {}:
            
            temp_freq_itemset = conditional_fp(order, new_root, new_header_table, min_sup_count)
            
            for temp_fi, temp_sup_count in temp_freq_itemset.items():

                frequent_itemset[temp_fi + (item,)] = temp_sup_count
        

    return frequent_itemset

# -------------- FP-Growth Algorithm --------------------------------------------
def my_fpgrowth(transactions, min_sup):
    # --------- sort transactions --------------------------------
    
    # ------------ count items ------------
    
    gen = (i for t in transactions for i in t) # generator
    
    first_itemset = { key:value for key,value in Counter(gen).items() }
    
    n = len(first_itemset)

    order = { key:n-i for (key, value), i in \
             zip( sorted(first_itemset.items(), key=lambda x:x[1]) , range(n) ) }
    
    # ------------- sort transactio based on order ----
    sorted_transactions = [ sorted(t, key=lambda x:order[x]) for t in transactions]
    
    root, header_table = fptree(order, sorted_transactions) # construct fp-tree
    
    # -------- construct conditional fp tree and generate frequent itemsets ---------------------
    
    min_sup_count = min_sup * len(transactions)
    
    frequent_itemsets = conditional_fp(order, root, header_table, min_sup_count)
    
    return frequent_itemsets


def diff(a, b): # diff that preserve order !
    sb = set(b)
    return tuple([i for i in a if i not in sb])

# ----------------- generate next rules -----------------------
def gen_candidates(k_itemset):
    
    n = len(k_itemset) # length Frequent Itemset
    i = 0
    
    while( i < n ):
        
        *remaining , last = k_itemset[i]
        
        i = i + 1
        
        last_items = [last]
        
        while( i < n ):
            
            *remaining_other , last_other = k_itemset[i]
            
            if remaining == remaining_other:
                
                last_items.append(last_other)
                
                i = i + 1
                
            else:
                break
        
        
        for a, b in itertools.combinations(last_items, 2):
            
            id1 = tuple(remaining) + (a,)
            id2 = (b,)
            
            items = id1 + id2
            
            yield items

# -------------- gen rules -----------------------------
def rules_my_fpgrowth(freq_itemset ,min_conf=0):
    
    # --------- fundtion that calculate counts ---------
    def count(itemset):
        return freq_itemset[itemset]
    
    # ---------------------------------------------------
    
    for item_list in freq_itemset:
        
        if len(item_list) == 1: continue
        
        S = item_list
        
        c = count(item_list)
        
#         yield (S, tuple(), c) # if u dont want have rules that Y is empty
    
        # ----- generate first rules
        y_list = []
            
        for item in item_list:
            Y = (item,)
            
            X = diff(S, Y)
            
            cx = count(X)
            
            conf = c / cx
        
            if conf >= min_conf:
                
                y_list.append(Y)
                
                yield (X, Y, conf)
        
        n = len(S)
        for i in range(2,n):
        
            chosen = []
        
            for condidate in gen_candidates(y_list):
                
                Y = condidate
                
                X = diff(S, Y)
            
                cx = count(X)
                
                conf = c / cx 
        
                if conf >= min_conf:
                
                    chosen.append(Y)
                
                    yield (X, Y, conf)
                
            y_list = chosen
            
            if not any(y_list): break

