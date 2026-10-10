"""One-bit Gaussian quantization and finite distortion-channel identities."""
import math
from information_theory.numerics import binary_entropy, channel_joint, mutual_information

def run(output_dir):
    threshold_results=[]
    for j in range(-40,41):
        z=j/10;phi=math.exp(-z*z/2)/math.sqrt(2*math.pi);cdf=(1+math.erf(z/math.sqrt(2)))/2
        d=1-phi*phi/(cdf*(1-cdf));threshold_results.append((z,d))
    scalar=1-2/math.pi;rd=[]
    for d in (0,.1,.2,.4,.5):
        w=((1,0),(2*d,1-2*d));mi=mutual_information(channel_joint((.5,.5),w))
        formula=binary_entropy(.5-d)-.5*binary_entropy(2*d)
        rd.append({'distortion':d,'direct_mi':mi,'formula':formula})
    alpha=.1;beta=.2;a=2;b=1
    joint=channel_joint((.5,.5),((1-alpha,alpha),(beta,1-beta)))
    asym=mutual_information(joint);asym_formula=binary_entropy((1+alpha-beta)/2)-.5*(binary_entropy(alpha)+binary_entropy(beta))
    return {'seed':0,'results':{'scalar_reproduction_magnitude_sigma_units':math.sqrt(2/math.pi),'scalar_distortion_variance_units':scalar,'block_distortion_variance_units':.25,'scalar_to_block_ratio':scalar/.25,'threshold_grid_minimum':min(threshold_results,key=lambda z:z[1]),'one_sided_rate_distortion_checks':rd,'asymmetric_example':{'a':a,'b':b,'alpha':alpha,'beta':beta,'distortion':(a*alpha+b*beta)/2,'mutual_information':asym}},'checks':{'threshold_grid_optimum':min(threshold_results,key=lambda z:z[1])[0]==0,'gaussian_ratio':all(d+1e-12>=scalar for z,d in threshold_results),'forbidden_channel_mi':all(abs(v['direct_mi']-v['formula'])<1e-14 for v in rd),'rate_decreasing':all(rd[i]['formula']>=rd[i+1]['formula'] for i in range(len(rd)-1)),'asymmetric_formula':abs(asym-asym_formula)<1e-14},'source_files':['src/information_theory/numerics.py']}
