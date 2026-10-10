"""Finite-channel identities and zero-error code verification for 7.1–7.14."""
import math
from information_theory.numerics import binary_entropy, channel_joint, mutual_information

def run(output_dir):
    mi=lambda p,w:mutual_information(channel_joint(p,w))
    z=((1,0),(.5,.5))
    unused=((2/3,1/3,0),(1/3,1/3,1/3),(0,1/3,2/3))
    code=[(i,2*i%5) for i in range(5)]
    def out(pair):
        return {((pair[0]+a)%5,(pair[1]+b)%5) for a in (-1,1) for b in (-1,1)}
    no_overlap=all(not(out(a)&out(b)) for i,a in enumerate(code) for b in code[i+1:])
    perm=((0,1,0,0),(0,0,1,0),(0,0,0,1),(1,0,0,0))
    pair_mi=mi((.25,)*4,perm)
    coordinate_fair=mutual_information(((.25,.25),(.25,.25)))
    coordinate_restricted=mutual_information(((.5,0),(0,.5)))
    cyclic=tuple(tuple(1/3 if (y-x)%11 in (1,2,3) else 0 for y in range(11)) for x in range(11))
    cyclic_mi=mi((1/11,)*11,cyclic)
    results={'mod_11_capacity':math.log2(11/3),'typewriter_noiseless':math.log2(26),'typewriter_noisy':math.log2(13),'z_capacity':mi((.6,.4),z),'z_fair_rate':mi((.5,.5),z),'pentagon_capacity':math.log2(5)-1,'pentagon_zero_error_capacity':math.log2(5)/2,'pentagon_code':code,'unused_symbol_capacity':mi((.5,0,.5),unused),'permutation_pair_capacity':pair_mi,'permutation_coordinate_fair':coordinate_fair,'permutation_coordinate_restricted':coordinate_restricted,'mod11_direct_mi':cyclic_mi}
    return {'seed':0,'results':results,'checks':{'permutation_checks':abs(pair_mi-2)<1e-14 and abs(coordinate_fair)<1e-14 and abs(coordinate_restricted-1)<1e-14,'cyclic_direct_check':abs(cyclic_mi-math.log2(11/3))<1e-13,'z_capacity_formula':abs(results['z_capacity']-math.log2(1.25))<1e-14,'z_fair_formula':abs(results['z_fair_rate']-(binary_entropy(.25)-.5))<1e-14,'pentagon_zero_error':no_overlap,'pentagon_rate_exceeds_one':results['pentagon_zero_error_capacity']>1,'unused_capacity':abs(results['unused_symbol_capacity']-2/3)<1e-14},'source_files':['src/information_theory/numerics.py']}
