"""Deterministic finite checks supporting Chapter 2 constructions."""
from math import log2, isclose
from itertools import product

def entropy(p):
    return -sum(x*log2(x) for x in p if x)

def identify(state):
    """Return predicted (coin, +/-1), or None, and actual outcomes."""
    path=[]
    def weigh(left,right):
        assert len(left)==len(right) and not set(left)&set(right)
        delta=0 if state is None else state[1]*((state[0] in left)-(state[0] in right))
        v=(delta>0)-(delta<0); path.append(v); return v
    first=weigh([1,2,3,4],[5,6,7,8])
    if first==0:
        second=weigh([9,10,11],[1,2,3])
        if second==0:
            third=weigh([12],[1]); ans=None if not third else (12,third)
        else:
            third=weigh([9],[10])
            ans=(11,second) if third==0 else ((9,second) if third==second else (10,second))
    else:
        swap=lambda x: x+4 if first<0 and x<=4 else x-4 if first<0 and x<=8 else x
        def w(left,right): return weigh(list(map(swap,left)),list(map(swap,right)))
        second=w([1,2,5],[3,6,9])
        if second>0:
            third=w([1],[2]); ans=(1,1) if third>0 else (2,1) if third<0 else (6,-1)
        elif second<0:
            third=w([3],[9]); assert third>=0; ans=(3,1) if third else (5,-1)
        else:
            third=w([7],[8]); ans=(4,1) if not third else (7,-1) if third<0 else (8,-1)
        ans=(swap(ans[0]),ans[1])
    return ans,tuple(path)

def run(output_dir):
    states=[None]+list(product(range(1,13),[-1,1]))
    decoded=[identify(s) for s in states]
    hx=entropy([2/3,1/3]); hxy=log2(3)
    results={"seed":0,"randomness":"none; exact exhaustive finite state enumeration", "counterfeit_states":len(states),"distinct_paths":len({p for _,p in decoded}),"max_weighings":max(len(p) for _,p in decoded),"ex_2_12":{"H_X":hx,"H_Y":hx,"H_X_given_Y":2/3,"H_Y_given_X":2/3,"H_XY":hxy,"I_X_Y":2*hx-hxy}}
    checks={"every_hypothesis_correct":all(s==a for s,(a,_) in zip(states,decoded)),"25_distinct_paths":len({p for _,p in decoded})==25,"three_weighing_budget":all(len(p)<=3 for _,p in decoded),"entropy_chain_rule":isclose(hxy,hx+2/3,abs_tol=1e-14)}
    return {"results":results,"checks":checks,"source_files":[],"artifacts":["artifacts/ch02/ex-2-12-venn.svg"]}
