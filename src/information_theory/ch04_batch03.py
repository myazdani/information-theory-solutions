"""Exact finite-block enumeration for the modulo-three increment process."""
from fractions import Fraction
from itertools import product
from math import log2,isclose
from .numerics import entropy

def run(output_dir):
    rows={};law=[Fraction(1,2),Fraction(1,4),Fraction(1,4)]
    checks={}
    for n in range(1,7):
        probabilities=[];bijective=set();independent=True
        for x in product(range(3),repeat=n):
            p=Fraction(1,3)
            for i in range(1,n):p*=law[(x[i]-x[i-1])%3]
            z=(x[0],)+tuple((x[i]-x[i-1])%3 for i in range(1,n));bijective.add(z)
            q=Fraction(1,3)
            for v in z[1:]:q*=law[v]
            independent &= p==q;probabilities.append(float(p))
        h=entropy(probabilities);rows[str(n)]={'block_entropy':h,'formula':log2(3)+(n-1)*1.5,'words':len(probabilities)}
        checks[f'n{n}_bijective']=len(bijective)==3**n
        checks[f'n{n}_factorization']=independent
        checks[f'n{n}_entropy']=isclose(h,rows[str(n)]['formula'],abs_tol=1e-12)
    return {'seed':0,'dependencies':[],'results':{'blocks':rows,'stationary_state_entropy':log2(3),'increment_entropy':entropy(law)},'checks':checks,'source_files':['src/information_theory/numerics.py']}
