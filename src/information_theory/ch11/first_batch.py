"""Checks for the inequality-projection counterexample and variance-estimator risks."""
from information_theory.numerics import relative_entropy

def run(output_dir):
    q=(1/3,)*3;p=(2/5,3/10,3/10);r=(9/20,9/20,1/10);s=(18/35,27/70,1/10)
    risks=[{'n':n,'biased_mse':(2*n-1)/n**2,'unbiased_mse':2/(n-1)} for n in range(2,21)]
    # A fine rational grid independently tests the direct objective over the intersection.
    grid=[]
    for a in range(400,901):
        for c in range(0,101):
            b=1000-a-c
            if b>=0:grid.append(relative_entropy((a/1000,b/1000,c/1000),q))
    return {'seed':0,'results':{'11.4.reference':q,'11.4.first_projection':p,'11.4.direct_projection':r,'11.4.sequential_projection':s,'11.4.direct_divergence_to_Q_bits':relative_entropy(r,q),'11.4.sequential_divergence_to_Q_bits':relative_entropy(s,q),'11.4.direct_divergence_to_first_bits':relative_entropy(r,p),'11.4.sequential_divergence_to_first_bits':relative_entropy(s,p),'11.6.normalized_variance_estimator_risks':risks},'checks':{'projection_feasible':r[0]>=.4 and s[0]>=.4 and r[2]<=.1 and s[2]<=.1,'different_projections':r!=s,'sequential_objective_strictly_lower':relative_entropy(s,p)<relative_entropy(r,p),'direct_objective_strictly_lower':relative_entropy(r,q)<relative_entropy(s,q),'direct_grid_minimum':abs(min(grid)-relative_entropy(r,q))<1e-13,'biased_mse_lower':all(v['biased_mse']<v['unbiased_mse'] for v in risks)},'source_files':['src/information_theory/numerics.py']}
