"""Piecewise exact-density verification for the uniform-noise capacity construction."""
import math
from fractions import Fraction as F

def construct(length):
    n=length.numerator//length.denominator;r=length-n
    if not r:return [(F(j),F(1,n+1)) for j in range(n+1)]
    d=(n+1)*(n+2)
    return [(F(j),F(n+1-j,d)) for j in range(n+1)]+[(F(j)+r,F(j+1,d)) for j in range(n+1)]

def run(output_dir):
    cases=[];checks={}
    for L in (F(1,3),F(1),F(5,3),F(7,2),F(10,3)):
        n=L.numerator//L.denominator;r=L-n;atoms=construct(L)
        knots=sorted({x for x,_ in atoms}|{x+1 for x,_ in atoms})
        integral=F(0);h=0.;maxerr=F(0)
        for lo,hi in zip(knots,knots[1:]):
            y=(lo+hi)/2
            density=sum((p for x,p in atoms if x<y<x+1),F(0))
            frac=y-y.numerator//y.denominator
            target=F(1,n+2) if frac<r else F(1,n+1)
            maxerr=max(maxerr,abs(density-target));integral+=(hi-lo)*density
            if density:h-=float((hi-lo)*density)*math.log2(float(density))
        capacity=float(1-r)*math.log2(n+1)+float(r)*math.log2(n+2)
        key=str(L)
        checks[key+'.mass']=sum(p for x,p in atoms)==1
        checks[key+'.density']=maxerr==0
        checks[key+'.integral']=integral==1
        checks[key+'.entropy']=abs(h-capacity)<1e-13
        cases.append({'scaled_input_width':key,'atoms':[[str(x),str(p)] for x,p in atoms],'entropy_bits':h,'capacity_formula_bits':capacity,'maximum_density_error':float(maxerr)})
    return {'seed':0,'results':{'cases':cases},'checks':checks,'source_files':[]}
