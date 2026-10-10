"""Residual-code tests and uniform-source redundancy calculations."""
from math import log,log2,floor,ceil,isclose
from .numerics import entropy

def sardinas(code):
    s={b[len(a):] for a in code for b in code if a!=b and b.startswith(a)}
    while True:
        if s&set(code):return False,sorted(s)
        new=set(s)
        for u in s:
            for c in code:
                if c.startswith(u) and c!=u:new.add(c[len(u):])
                if u.startswith(c) and c!=u:new.add(u[len(c):])
        if new==s:return True,sorted(s)
        s=new

def run(output_dir):
    cases=[['0','10','11'],['0','01','11'],['0','01','10'],['0','01'],['00','01','10','11'],['110','11','10'],['110','11','100','00','10']]
    decoded=[{'code':c,'uniquely_decodable':sardinas(c)[0],'residual_closure':sardinas(c)[1]} for c in cases]
    rows=[];checks={}
    for k in range(13):
        def red(m):return k+2-2**(k+1)/m-log2(m)
        choices={max(2**k,min(2**(k+1),v)) for v in [floor(2**(k+1)*log(2)),ceil(2**(k+1)*log(2))]}
        best=max(choices,key=red);allbest=max(range(2**k,2**(k+1)+1),key=red)
        rows.append({'k':k,'maximizing_m':best,'redundancy':red(best)})
        checks[f'k{k}_integer_maximizer']=isclose(red(best),red(allbest),abs_tol=1e-14)
    checks['SP_expected_results']=[z['uniquely_decodable'] for z in decoded]==[True,True,False,True,True,True,True]
    checks['ambiguity_witness']='0'+'10'=='01'+'0'
    checks['Shannon_dyadic_entropy']=isclose(entropy([.5,.25,.125,.125]),1.75)
    return {'seed':0,'dependencies':[],'results':{'ex_5_24':{'limiting_max_redundancy':2-1/log(2)-log2(2*log(2)),'integer_maxima':rows},'ex_5_27':decoded,'ex_5_28':{'codes':['0','10','110','111'],'average_length':1.75}},'checks':checks,'source_files':['src/information_theory/numerics.py']}
