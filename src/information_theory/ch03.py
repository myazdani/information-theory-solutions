"""Exact binomial counts and threshold-set computations for Chapter 3."""
from fractions import Fraction
from math import comb,log2,ceil,log,exp,isclose
import csv
from .numerics import entropy,binary_entropy

def run(output_dir):
    n=100;p=Fraction(1,200)
    number=sum(comb(n,k) for k in range(4));failure=sum(Fraction(comb(n,k))*p**k*(1-p)**(n-k) for k in range(4,101))
    h=binary_entropy(.6);n=25;p=Fraction(3,5)
    rows=[]
    for k in range(n+1):
        seq=p**k*(1-p)**(n-k);surp=-log2(float(seq))/n
        rows.append({'ones':k,'count':comb(n,k),'sequence_probability':float(seq),'class_probability':float(comb(n,k)*seq),'surprisal_per_symbol':surp,'typical':abs(surp-h)<=.1})
    ks=[a['ones'] for a in rows if a['typical']];tcount=sum(comb(n,k) for k in ks);tmass=sum(Fraction(comb(n,k))*p**k*(1-p)**(n-k) for k in ks)
    target=Fraction(9,10);mass=Fraction(0);count=0;selected={};before_last=Fraction(0)
    for k in reversed(range(n+1)):
        prob=p**k*(1-p)**(n-k);need=min(comb(n,k),max(0,ceil((target-mass)/prob)))
        if need:
            before_last=mass+(need-1)*prob
            selected[k]=need;count+=need;mass+=need*prob
        if mass>=target:break
    icount=sum(v for k,v in selected.items() if k in ks);imass=sum(v*p**k*(1-p)**(n-k) for k,v in selected.items() if k in ks)
    path=output_dir/'ex-3-13-binomial.csv'
    with path.open('w') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    results={'ex_3_3':{'exponent_bits':-.75*log2(2/3)-.25*log2(3/5),'base':(2/3)**.75*(3/5)**.25},'ex_3_7':{'codewords':number,'length':ceil(log2(number)),'failure_probability':float(failure),'Chebyshev_bound':.4975/3.5**2},'ex_3_8_limit':6**.25,'ex_3_10_limit':exp(-1),'ex_3_13':{'entropy':h,'typical_weights':ks,'typical_count':tcount,'typical_probability':float(tmass),'smallest_90pct_count':count,'smallest_set_weights_and_counts':selected,'smallest_set_probability':float(mass),'intersection_count':icount,'intersection_probability':float(imass)}}
    checks={'code_length_minimal':2**(ceil(log2(number))-1)<number<=2**ceil(log2(number)),'Chebyshev_upper_bound':float(failure)<.4975/3.5**2,'typical_weights_11_to_19':ks==list(range(11,20)),'minimal_cardinality_crosses_target':before_last<target<=mass,'binomial_mass_sums_to_one':sum(Fraction(comb(n,k))*p**k*(1-p)**(n-k) for k in range(n+1))==1,'typical_mass_direct_sum':isclose(float(tmass),sum(a['class_probability'] for a in rows if a['typical']))}
    return {'seed':0,'dependencies':[],'results':results,'checks':checks,'source_files':['src/information_theory/numerics.py'],'artifacts':['artifacts/ch03/ex-3-13-binomial.csv']}
