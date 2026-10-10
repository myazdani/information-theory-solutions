"""Priced water filling and the film-grain small-cell limit."""
import math
from information_theory.numerics import binary_entropy

def run(output_dir):
    b=(1,2);noise=(3,2);budget=10
    level=(budget+sum(c*n for c,n in zip(b,noise)))/2
    powers=[level/c-n for c,n in zip(b,noise)]
    capacity=sum(math.log2(1+p/n)/2 for p,n in zip(powers,noise))
    limit=1/(math.e*math.log(2));cells=[]
    for alpha in (1e-2,1e-3,1e-4,1e-5):
        t=2**(-binary_entropy(alpha)/alpha)
        cells.append({'occupancy':alpha,'capacity_per_occupancy':math.log1p(t)/math.log(2)/alpha,'optimal_illumination':t/(alpha*(1+t))})
    return {'seed':0,'results':{'9.8.powers':powers,'9.8.capacity_bits':capacity,'9.10.bits_per_grain_limit':limit,'9.10.small_cell_checks':cells},'checks':{'budget':abs(sum(c*p for c,p in zip(b,powers))-budget)<1e-13,'equal_marginal_gain':abs(b[0]*(noise[0]+powers[0])-b[1]*(noise[1]+powers[1]))<1e-13,'capacity_formula':abs(capacity-.5*math.log2(289/48))<1e-13,'film_limit':abs(cells[-1]['capacity_per_occupancy']-limit)<1e-5,'illumination_limit':abs(cells[-1]['optimal_illumination']-1/math.e)<1e-5},'source_files':['src/information_theory/numerics.py']}
