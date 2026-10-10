"""Exact conditional counts and seeded simplex sampler moment checks."""
import math
import random
from fractions import Fraction as F

def run(output_dir):
    seed=20261010;rng=random.Random(seed);n=3;samples=50000
    sums=[0.,0.,0.];sums2=[0.,0.,0.]
    for _ in range(samples):
        uniforms=[rng.random() for _ in range(n)];a=uniforms[0]/sum(uniforms)
        exponentials=[rng.expovariate(1) for _ in range(n)];b=exponentials[0]/sum(exponentials)
        cuts=sorted(rng.random() for _ in range(n-1));c=cuts[0]
        for i,x in enumerate((a,b,c)):sums[i]+=x;sums2[i]+=x*x
    means=[v/samples for v in sums];vars_=[sums2[i]/samples-means[i]**2 for i in range(3)]
    target=(n-1)/(n*n*(n+1));counts_a=[];counts_b=[]
    for k in (4,8,100):
        ratio=F(math.comb(k-1,k//4-1),math.comb(k,k//4));counts_a.append({'n':k,'conditional_probability':str(ratio)})
    for k in (2,4,10,100):
        ratio=F(math.comb(k-1,k//2-1)*2**(k//2-1),math.comb(k,k//2)*2**(k//2));counts_b.append({'n':k,'conditional_probability':str(ratio)})
    return {'seed':seed,'results':{'11.26.bernoulli_exact_counts':counts_a,'11.26.three_symbol_exact_counts':counts_b,'11.29.dimension':n,'11.29.samples_per_method':samples,'11.29.methods':['normalized_uniforms','normalized_exponentials','uniform_cut_spacings'],'11.29.coordinate_means':means,'11.29.coordinate_variances':vars_,'11.29.uniform_simplex_theoretical_mean':1/n,'11.29.uniform_simplex_theoretical_variance':target},'checks':{'bernoulli_exact_quarter':all(v['conditional_probability']=='1/4' for v in counts_a),'three_symbol_exact_quarter':all(v['conditional_probability']=='1/4' for v in counts_b),'simplex_means':all(abs(x-1/n)<.004 for x in means),'exponential_variance':abs(vars_[1]-target)<.0015,'spacing_variance':abs(vars_[2]-target)<.0015,'normalized_uniform_not_uniform':vars_[0]<target-.01},'source_files':[]}
