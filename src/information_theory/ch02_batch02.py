"""Reproducible enumeration and quadrature for Exercises 2.17, 2.18, 2.24."""
from itertools import product
from collections import Counter, defaultdict
from math import log, log2, isclose
from .numerics import entropy, binary_entropy

def run(output_dir):
    classes=defaultdict(list)
    for x in product(range(2),repeat=4):classes[sum(x)].append(x)
    mapping={}
    for k,words in classes.items():
        for j,w in enumerate(words):mapping[w]='' if k in [0,4] else format(j,'02b') if j<4 else str(j-4)
    fair=all(len({sum(1 for x,o in mapping.items() if sum(x)==k and o==z) for z in (format(j,f'0{length}b') for j in range(2**length))})==1 for k in range(5) for length in [1,2])
    outcomes=[]
    def series(s):
        if s.count('A')==4 or s.count('B')==4:outcomes.append(s);return
        series(s+'A');series(s+'B')
    series('');dist=Counter(len(s) for s in outcomes);py=[dist[j]*2**(-j) for j in range(4,8)]
    hx=entropy([2**(-len(s)) for s in outcomes]);hy=entropy(py)
    n=100000
    avg=sum(binary_entropy((i+.5)/n) for i in range(n))/n
    result={"extractor_words":16,"extractor_EK_at_half":sum(map(len,mapping.values()))/16,"series_counts":dict(dist),"series_length_probabilities":py,"series_H_X":hx,"series_H_Y":hy,"series_H_X_given_Y":hx-hy,"H_quarter":binary_entropy(.25),"binary_entropy_uniform_p_midpoint_integral":avg,"binary_entropy_uniform_p_exact":1/(2*log(2)),"simplex_3_expected_entropy":5/(6*log(2)),"quadrature_intervals":n}
    checks={"extractor_fair_every_type":fair,"extractor_mean":isclose(result['extractor_EK_at_half'],13/8),"series_probability_normalized":isclose(sum(py),1),"series_H_X_equals_expected_length":isclose(hx,93/16),"series_H_Y_formula":isclose(hy,27/8-5*log2(5)/8),"quadrature_error_below_1e-9":abs(avg-1/(2*log(2)))<1e-9}
    return {"seed":0,"dependencies":[],"results":result,"checks":checks,"source_files":["src/information_theory/numerics.py"]}
