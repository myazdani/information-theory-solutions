"""Exact finite-source calculations for the remaining Chapter 5 examples."""
from fractions import Fraction
from math import log2,ceil,isclose
from itertools import product
from .numerics import entropy,relative_entropy
from .ch05_batch01 import huffman

def run(output_dir):
    p=[Fraction(1,2),Fraction(1,4),Fraction(1,8),Fraction(1,16),Fraction(1,16)]
    q=[Fraction(1,2)]+[Fraction(1,8)]*4;l1=[1,2,3,4,4];l2=[1,3,3,3,3]
    mean=lambda probs,lengths:float(sum(a*b for a,b in zip(probs,lengths)))
    wine=huffman([8,6,4,2,2,1]);binary=huffman([6,6,4,4,3,2],2);quaternary=huffman([6,6,4,4,3,2],4)
    alphabet=['A','B','C','A0','A1','B0'];outputs={};unique=True
    for n in range(1,5):
        for source in product(range(6),repeat=n):
            encoded=''.join(alphabet[i] for i in source)
            if encoded in outputs and outputs[encoded]!=source:unique=False
            outputs[encoded]=source
    results={'ex_5_30':{'H_p':entropy(p),'H_q':entropy(q),'D_p_q':relative_entropy(p,q),'D_q_p':relative_entropy(q,p),'L_C1_p':mean(p,l1),'L_C2_q':mean(q,l2),'L_C2_p':mean(p,l2),'L_C1_q':mean(q,l1)},'ex_5_31_uniform_three':{'nonsingular_mean':4/3,'entropy':log2(3)},'ex_5_32':{'sequential_mean':Fraction(55,23).__float__(),'sequential_mean_exact':'55/23','mixture_huffman':wine},'ex_5_33':{'binary_huffman_lengths':huffman([6,3,1])['lengths'],'binary_Shannon_lengths':[ceil(-log2(p)) for p in [.6,.3,.1]],'minimum_D_equal_means':10},'ex_5_38':{'binary':binary,'quaternary':quaternary},'ex_5_40':{'source_rate':1.5,'case_a_rate':1.,'case_b_rate':.75,'case_c_rate':6/7,'case_c_mean_length':1.75},'ex_5_43':{'uniquely_decodable_code':alphabet,'mean':95/69,'prefix_only_mean':2.},'ex_5_44':{'length_6_count':28,'length_7_count':72,'average_length':6.72}}
    checks={'dyadic_codes_match_entropy':isclose(mean(p,l1),entropy(p)) and isclose(mean(q,l2),entropy(q)),'mismatch_loss_matches_KL':isclose(mean(p,l2)-entropy(p),relative_entropy(p,q)) and isclose(mean(q,l1)-entropy(q),relative_entropy(q,p)),'wine_mixture_better':wine['average_length']<55/23,'marker_code_no_collision_through_4_symbols':unique,'hundred_symbol_Kraft':Fraction(28,64)+Fraction(72,128)==1,'quaternary_prefix':all(not b.startswith(a) for i,a in enumerate(quaternary['codes']) for j,b in enumerate(quaternary['codes']) if i!=j)}
    return {'seed':0,'dependencies':[],'results':results,'checks':checks,'source_files':['src/information_theory/numerics.py','src/information_theory/ch05_batch01.py']}
