"""Deterministic arithmetic for Chapter 6; no random sampling is used."""
import math
from information_theory.numerics import entropy, relative_entropy

def run(output_dir):
    p=(.5,.25,.25); f=(1/8,1/8,1/4,1/16,1/16,1/16,1/4,1/16)
    lotto_drift=sum(math.log2(1/(8*v))/8 for v in f)
    card_h=math.log2(math.comb(52,26))
    race_h=entropy(p)
    rate_public=sum(a*math.log2(a*o) for a,o in zip(p,(4,4,2)))
    dutch_b=30/(10+30); dutch_factor=10*dutch_b
    dutch_rate=math.log2(dutch_factor)
    log_opt_rate=sum(math.log2(.5*o)/2 for o in (10,30))
    results={
        '6.1.optimal_bits':math.log2(3)-race_h,
        '6.3.marginal_bits':entropy((.5,.5)),
        '6.3.joint_bits':card_h,
        '6.4.optimal_bits':52-card_h,
        '6.5.entropy_bits':race_h,
        '6.5.optimal_bits':rate_public,
        '6.5.polynomial_at_optimum':128*p[0]**2*p[1]*p[2],
        '6.7.geometric_wealth':100*2**(20*(2-entropy((.5,.25,.125,.125)))),
        '6.7.expected_wealth':100*(4*sum(v*v for v in (.5,.25,.125,.125)))**20,
        '6.8.growth_bits':lotto_drift,
        '6.8.typical_days':math.log2(10**6)/lotto_drift,
        '6.8.expected_first_passage_days':math.ceil(math.log2(10**6))/lotto_drift,
        '6.10.optimal_bits':sum(a*math.log2(a*o) for a,o in zip(p,(4,3,3))),
        '6.10.misspecified_bits':sum(a*math.log2(b*o) for a,b,o in zip(p,(.25,.5,.25),(4,3,3))),
        '6.13.dutch_bet':dutch_b,
        '6.13.sure_factor':dutch_factor,
        '6.13.sure_growth_bits':dutch_rate,
        '6.13.optimal_growth_bits':log_opt_rate,
        '6.13.growth_gap_bits':log_opt_rate-dutch_rate,
    }
    return {'seed':0,'results':results,'checks':{
        'positive_growth':results['6.1.optimal_bits']>0,
        'card_count_symmetry':math.comb(52,26)==math.comb(51,25)+math.comb(51,26),
        'public_rate_identity':abs(rate_public-relative_entropy(p,(.25,.25,.5)))<1e-14,
        'polynomial_rate_identity':abs(rate_public-math.log2(results['6.5.polynomial_at_optimum'])/4)<1e-14,
        'lottery_drift':abs(lotto_drift-.25)<1e-14,
        'misspecification_loss':abs(results['6.10.optimal_bits']-results['6.10.misspecified_bits']-relative_entropy(p,(.25,.5,.25)))<1e-14,
        'first_passage_ceiling':results['6.8.expected_first_passage_days']==80,
        'geometric_below_mean':results['6.7.geometric_wealth']<results['6.7.expected_wealth'],
        'dutch_equalization':abs(10*dutch_b-30*(1-dutch_b))<1e-14,
        'dutch_gap_identity':abs(log_opt_rate-dutch_rate-.5*math.log2(4/3))<1e-14,
    },'source_files':['src/information_theory/numerics.py']}
