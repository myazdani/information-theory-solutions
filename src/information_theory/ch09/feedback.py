"""Bisection solution and direct covariance verification for two-use feedback."""
import math

def optimize(power,rho):
    if not math.isfinite(power) or power<0 or not math.isfinite(rho) or abs(rho)>=1:
        raise ValueError("Require finite power >= 0 and |rho| < 1 for nonsingular covariance.")
    r=abs(rho);q=2*power
    if power==0:
        return {"power":0,"rho":rho,"first_power":0,"feedback_coefficient":0,"input_correlation_coefficient":0,"determinant":1-r*r,"direct_determinant":1-r*r,"total_power":0,"feedback_information":0,"nonfeedback_information":0,"grid_max_determinant":1-r*r}
    def f(a):return (1+a)*(1+q-a)-r*r+2*r*math.sqrt(max(0,a*(1+a)*(q-a)))
    def df(a):
        g=a*(1+a)*(q-a)
        return q-2*a+r*(q+2*(q-1)*a-3*a*a)/math.sqrt(g)
    if r==0:a=power
    else:
        lo=power;hi=q
        for _ in range(100):
            mid=(lo+hi)/2
            if mid==lo or mid==hi:break
            if df(mid)>0:lo=mid
            else:hi=mid
        a=(lo+hi)/2
    sign=1 if rho>=0 else -1
    b=sign*math.sqrt(a*(q-a)/(1+a))
    u=-sign*math.sqrt((q-a)/(a*(1+a)))
    d=a*u*u+b*b
    y11=1+a;y22=d+1+2*b*rho;y12=a*u+rho+b
    direct=y11*y22-y12*y12
    nf=.5*math.log2(1+2*power/(1-r)) if power<=r else .5*math.log2((1+power)**2/(1-r*r))
    gridmax=max(f(q*i/10000) for i in range(10001))
    return {'power':power,'rho':rho,'first_power':a,'feedback_coefficient':b,'input_correlation_coefficient':u,'determinant':f(a),'direct_determinant':direct,'total_power':a+d,'feedback_information':.5*math.log2(f(a)/(1-r*r)),'nonfeedback_information':nf,'grid_max_determinant':gridmax}

def run(output_dir):
    rows=[optimize(p,r) for p in (0,.1,1,5) for r in (0,.25,-.8)]
    checks={}
    for i,row in enumerate(rows):
        checks[f'{i}.power']=abs(row['total_power']-2*row['power'])<1e-12
        checks[f'{i}.covariance']=abs(row['direct_determinant']-row['determinant'])<1e-11
        checks[f'{i}.grid_upper']=row['determinant']+1e-11>=row['grid_max_determinant']
        checks[f'{i}.feedback_gain']=row['feedback_information']+1e-12>=row['nonfeedback_information']
    return {'seed':0,'results':{'cases':rows},'checks':checks,'source_files':[]}
