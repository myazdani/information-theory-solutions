"""Exact rational check of the printed same-epsilon typicality claim."""
from fractions import Fraction as F

def run(output_dir):
    n=100;ones=54;eps=F(1,10)
    counts=(n-ones,ones);deviations=[abs(F(k,n)-F(1,2)) for k in counts]
    marginal=all(d<eps/2 for d in deviations)
    # For Y=X, off-diagonal types must have zero counts; the diagonal counts are forced.
    candidates=[((n-ones,0),(0,ones))]
    feasible=[]
    for table in candidates:
        if all(abs(F(table[i][i],n)-F(1,2))<eps/4 for i in range(2)):feasible.append(table)
    return {'seed':0,'results':{'n':n,'ones':ones,'epsilon':str(eps),'marginal_deviations':[str(d) for d in deviations],'marginal_threshold':str(eps/2),'joint_threshold':str(eps/4),'is_marginally_typical':marginal,'forced_joint_counts':candidates[0],'joint_section_nonempty':bool(feasible)},'checks':{'marginal_typical':marginal,'joint_empty':not feasible,'same_tolerance_counterexample':marginal and all(d>eps/4 for d in deviations)},'source_files':[]}
