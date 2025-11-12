import itertools # for generating k+1
from collections import defaultdict

# ----------- funtion to build the initial first faze (1-length frequent elemnt set) --------------
def initial(transactions, min_sup):
    
        temp = defaultdict(set)
        
        T = len(transactions)
        
        
        for t_id in range(T):
            
            transaction = transactions[t_id]
            
            for item in transaction:
            
                if item in temp:
                
                    temp[item].add(t_id)
                
            
                else: # --- if we never created an item
                
                    pl = set([t_id]) # pl : posting list
                    
                    temp[item] = pl
                    
        # -------------- bulid freq_1 and map ------------------
        
        itemsets = defaultdict(dict)
        
        postinglist = defaultdict(set)
        
        index = 0
        for k,v in sorted(temp.items(), key=lambda x: len(x[1]) ):
        
            freq = len(temp[k])
            
            if ( freq / T ) >= min_sup:
                
                tuple_index = (k,)
                
                itemsets[1][tuple_index] = freq
                
                postinglist[k] = temp[k]
            
        
        
        return itemsets, postinglist

# ----------------- gen_next_nodes -----------------------
# This function is based on the Efficient-Apriori project:
# https://github.com/tommyod/Efficient-Apriori
# Original MIT License applies.
# Original idea © Tommy Odhiambo.
# Modified implementation © Navid Razman.
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
            
# ------------------ apriori algorithm ----------------------
def my_apriori(transactions, min_sup = 0.85):
        
    # ----------------- find support -----------------------
    def frequnecy(item_list):
        
        if any(item_list):
            
            postlists = [ postinglist[name] for name in item_list ]
    
            I = set.intersection(*postlists)
        
            c = len(I)
            
            return c
        
        else:
            
            return 0
    

                
    # ---------------------------------------------------------
    k = 1
    
    T = len(transactions)
    
    itemsets, postinglist = initial(transactions, min_sup)
    
    freq_itemset =  list(itemsets[k].keys()) # initial candidates
    
    yield  k, itemsets[k] 

    while True:
        # filter candidates
        k = k + 1
        
        for candidate in gen_candidates(freq_itemset):
            
            freq = frequnecy(candidate)
            
            if (freq / T) >= min_sup:
                
                itemsets[k][candidate] = freq
                
                
        freq_itemset =  list(itemsets[k].keys())
        
        if any(freq_itemset):
            
            yield  k, itemsets[k] # using generator for fast answer
            
        else:
            break  


# ---- function for dif that preserve order eg diff(a,b) != diff(b,a)
def diff(a, b): 
    sb = set(b)
    return tuple([i for i in a if i not in sb])


# ----------------- generate rules ---------------------
def rules_my_apriori(freq_itemsets ,min_conf):
    
    # --------- fundtion that calculate counts ---------
    def count(itemset):
        n = len(itemset)   
        return freq_itemsets[n][itemset]
    # ---------------------------------------------------
    
    for k in range( 1, len(freq_itemsets) ):
        
        for item_list in freq_itemsets[k+1]:

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

