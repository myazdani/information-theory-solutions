"""Testing exponents, six-state conditioning, and finite factorial checks."""
import math
from information_theory.numerics import relative_entropy

def run(output_dir):
    p1=(.5,.25,.25);p2=(.25,.25,.5)
    a=2**(1/3);z=4+a+a**-2;tilt=(a/z,a**-2/z,1/z,1/z,1/z,1/z)
    state_rate=relative_entropy(tilt,(1/6,)*6)
    geometric_rate=-math.log(2)+3*math.log(1.5)
    factorial=[{'n':n,'log_factorial':math.lgamma(n+1),'printed_log_upper':math.log(n)+n*(math.log(n)-1),'corrected_log_upper':1+math.log(n)+n*(math.log(n)-1)} for n in range(1,101)]
    return {'seed':0,'results':{'11.12.stein_exponent_bits':relative_entropy(p2,p1),'11.15.normalizer':z,'11.15.conditional_distribution':tilt,'11.15.exponent_bits':state_rate,'11.18.geometric_exponent_nats':geometric_rate,'11.18.geometric_exponent_bits':geometric_rate/math.log(2),'11.20.printed_upper_failures_1_to_100':[v['n'] for v in factorial if v['log_factorial']>v['printed_log_upper']+1e-12]},'checks':{'testing_direction_value':abs(relative_entropy(p2,p1)-.25)<1e-14,'state_ratio':abs(tilt[0]-2*tilt[1])<1e-14,'state_rate_formula':abs(state_rate-math.log2(6/z))<1e-14,'geometric_rate_formula':abs(geometric_rate-math.log(27/16))<1e-14,'corrected_factorial_bound':all(v['log_factorial']<=v['corrected_log_upper']+1e-12 for v in factorial),'large_n_printed_bound':all(v['log_factorial']<=v['printed_log_upper']+1e-12 for v in factorial if v['n']>=7)},'source_files':['src/information_theory/numerics.py']}
