"""Exact binomial probabilities and exhaustive three-bit code checks."""
import itertools
import math
from information_theory.numerics import binary_entropy, entropy, channel_joint, mutual_information

def run(output_dir):
    n=25;p=.1;eps=.2;m=512
    ks=[k for k in range(n+1) if abs(-math.log2(1-p)+k/n*math.log2((1-p)/p)-binary_entropy(p))<eps]
    t=sum(math.comb(n,k) for k in ks)
    s=sum(math.comb(n,k)*p**k*(1-p)**(n-k) for k in ks);q=t/2**n
    spurious=-math.expm1((m-1)*math.log1p(-q))
    pe=1-s*(1-q)**(m-1)
    pe_radius=1-(s+(1-p)**n)*(1-(t+1)/2**n)**(m-1)
    words=list(itertools.product((0,1),repeat=3))
    def w(y,x):
        d=sum(a!=b for a,b in zip(x,y));return p**d*(1-p)**(3-d)
    all_success=[sum(max(w(y,x) for x in code) for y in words)/4 for code in itertools.combinations(words,4)]
    code=[x for x in words if sum(x)%2==0]
    even_success=sum(max(w(y,x) for x in code) for y in words)/4
    def bec_error(code):
        success=0.
        for erased in itertools.product((0,1),repeat=3):
            prob=p**sum(erased)*(1-p)**(3-sum(erased))
            classes={tuple(x[i] for i in range(3) if not erased[i]) for x in code}
            success+=prob*len(classes)/len(code)
        return 1-success
    w4=((.5,.5,0,0),(0,.5,.5,0),(0,0,.5,.5),(.5,0,0,.5))
    wz=tuple((row[0]+row[1],row[2]+row[3]) for row in w4)
    coarse_odd=mutual_information(channel_joint((0,.5,0,.5),wz))
    coarse_even=mutual_information(channel_joint((.5,0,.5,0),wz))
    full_odd=mutual_information(channel_joint((0,.5,0,.5),w4))
    results={'7.26.coarse_odd_mi':coarse_odd,'7.26.coarse_even_mi':coarse_even,'7.26.full_odd_mi':full_odd,'7.15.HX':1,'7.15.HY':1,'7.15.HXY':1+binary_entropy(p),'7.15.I':1-binary_entropy(p),'7.15.typical_weights':ks,'7.15.typical_size':t,'7.15.true_typical_probability':s,'7.15.random_match_probability':q,'7.15.spurious_probability':spurious,'7.15.error_probability':pe,'7.15.radius4_error':pe_radius,'7.16.crossover':3*p*p*(1-p)+p**3,'7.16.effective_capacity_per_use':(1-binary_entropy(3*p*p*(1-p)+p**3))/3,'7.16.original_capacity':1-binary_entropy(p),'7.17.even_parity_bsc_error':1-even_success,'7.17.best_bsc_error_all_70_codes':1-max(all_success),'7.17.full_bsc_error':1-(1-p)**3,'7.17.repetition_bec_error':bec_error([(0,0,0),(1,1,1)]),'7.17.parity_bec_error':bec_error(code),'7.17.full_bec_error':bec_error(words),'7.18.b_capacity':math.log2(3)-1,'7.24.exceptional_uniform_rate':entropy([v/12 for v in (1,2,2,3,2,1,1)])-math.log2(3)}
    return {'seed':0,'results':results,'checks':{'coarse_channel_mi':abs(coarse_odd)<1e-14 and abs(coarse_even-1)<1e-14 and abs(full_odd-1)<1e-14,'typical_set':ks==[1,2,3,4] and t==15275,'spurious_identity':abs(spurious-(1-(1-q)**511))<1e-13,'parity_optimal':abs(max(all_success)-even_success)<1e-14,'parity_error':abs(1-even_success-.19)<1e-14,'bec_four_formula':abs(bec_error(code)-(.5*3*p*p*(1-p)+.75*p**3))<1e-14,'bec_eight_formula':abs(bec_error(words)-(1-(1-p/2)**3))<1e-14,'exceptional_noise_rate_exceeds_one':results['7.24.exceptional_uniform_rate']>1},'source_files':['src/information_theory/numerics.py']}
