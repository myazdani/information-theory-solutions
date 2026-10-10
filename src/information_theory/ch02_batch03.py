"""Direct computations and exhaustive card-move checks for Chapter 2."""
from collections import Counter
from math import log2,isclose
from .numerics import entropy,conditional_entropy,relative_entropy,binary_entropy

def run(output_dir):
    table=[[1/6 if i==j else 1/12 for j in range(3)] for i in range(3)]
    hcond=conditional_entropy(table);pe=1-sum(max(row) for row in zip(*table))
    p=[.5,.25,.25];q=[1/3]*3
    decks={};card_checks=[]
    for n in range(1,11):
        original=tuple(range(n));c=Counter()
        for i in range(n):
            shortened=original[:i]+original[i+1:]
            for j in range(n):c[shortened[:j]+(original[i],)+shortened[j:]]+=1
        h=entropy([v/n**2 for v in c.values()]);formula=(2-1/n)*log2(n)-2*(n-1)/n**2
        decks[str(n)]={"distinct_decks":len(c),"entropy":h,"formula":formula}
        card_checks.append(isclose(h,formula,abs_tol=1e-12))
    result={"ex_2_32":{"P_error":pe,"conditional_entropy":hcond,"textbook_Fano_bound":binary_entropy(pe)+pe*log2(3),"sharp_Fano_bound":binary_entropy(pe)+pe},"ex_2_35":{"H_p":entropy(p),"H_q":entropy(q),"D_p_q":relative_entropy(p,q),"D_q_p":relative_entropy(q,p)},"ex_2_36_common_divergence":relative_entropy([.25,.75],[.75,.25]),"ex_2_43_die_MI":log2(6)-log2(4),"ex_2_44_max_EK":1-3*(1/3)**2,"ex_2_47_decks":decks,"ex_2_48":{"H_N":binary_entropy(1/3),"H_word_given_N":10,"H_word":10+binary_entropy(1/3)}}
    checks={"Fano_P_error_half":isclose(pe,.5),"Fano_sharp_equality":isclose(hcond,binary_entropy(pe)+pe),"KL_asymmetry":abs(relative_entropy(p,q)-relative_entropy(q,p))>1e-3,"card_formula_all_n_1_to_10":all(card_checks),"reversed_binary_KL_equal":isclose(relative_entropy([.25,.75],[.75,.25]),relative_entropy([.75,.25],[.25,.75]))}
    return {"seed":0,"dependencies":[],"results":result,"checks":checks,"source_files":["src/information_theory/numerics.py"]}
