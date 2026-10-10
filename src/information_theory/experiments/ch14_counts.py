"""Small exact combinatorial checks and the substitution-key calculation."""
from collections import Counter
from math import factorial, log2, log, gcd

def equal_area_count(n):
    frequencies=Counter(w*h for w in range(1,n+1) for h in range(1,n+1))
    return sum(v*v for v in frequencies.values())

def ratio_count(n):
    return sum((n//max(a,b))**2 for a in range(1,n+1) for b in range(1,n+1) if gcd(a,b)==1)

def run(output_dir):
    key_bits=log2(factorial(27)); key_symbols=key_bits/log2(27)
    counts={str(n):equal_area_count(n) for n in [2,4,8,16,32]}
    return {'results':{'14.11':{'equal_area_dimension_quadruple_counts':counts},
                       '14.12':{'key_bits':key_bits,'key_27ary_symbols':key_symbols,'heuristic_unicity_characters':key_symbols/.75}},
            'checks':{'ratio_parameterization':all(equal_area_count(n)==ratio_count(n) for n in range(1,33)),
                      'count_bound':all(n*n<=equal_area_count(n)<=2*n*n*sum(1/m for m in range(1,n+1)) for n in range(1,33)),
                      'unicity_interval':26<key_symbols/.75<27},
            'seed':0,'dependencies':[],'source_files':[]}
