"""Entropy-rate optimizers and a stationary conditional-entropy counterexample."""
from math import sqrt,log2,isclose
from .numerics import binary_entropy,entropy

def run(output_dir):
    phi=(1+sqrt(5))/2;p=(3-sqrt(5))/2
    grid=[j/10000 for j in range(10001)]
    max_grid=max(binary_entropy(t)/(1+t) for t in grid)
    pi=[.5,.25,.25];P=[[0,.5,.5],[1,0,0],[1,0,0]]
    pinext=[sum(pi[i]*P[i][j] for i in range(3)) for j in range(3)]
    result={'golden_ratio':phi,'ex_4_7_optimal_p':p,'ex_4_7_max_rate':binary_entropy(p)/(1+p),'ex_4_8_optimal_p1':1/phi,'ex_4_8_max_rate':binary_entropy(1/phi)/(2-1/phi),'grid_step':1e-4,'grid_max_rate':max_grid,'ex_4_12_rate':binary_entropy(.1),'ex_4_12_expected_initial_run':10,'ex_4_4_stationary_after_transition':pinext,'ex_4_4_conditional_entropies':[entropy(P[0]),entropy([1,0,0])]}
    checks={'stationary_counterexample':pinext==pi,'counterexample_entropy_decreases':result['ex_4_4_conditional_entropies']==[1.,0.],'golden_ratio_optimality_equation':isclose((1-p)**2,p),'analytic_rate_matches_log_phi':isclose(result['ex_4_7_max_rate'],log2(phi)),'grid_below_analytic_optimum':max_grid<=log2(phi)+1e-14,'duration_rate_matches':isclose(result['ex_4_8_max_rate'],log2(phi))}
    return {'seed':0,'dependencies':[],'results':result,'checks':checks,'source_files':['src/information_theory/numerics.py']}
