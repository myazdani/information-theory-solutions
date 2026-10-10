"""Exact two-day portfolio arithmetic, universality factors, and wealth plot."""
from fractions import Fraction as F
from math import comb, log2, isclose
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/information-theory-matplotlib')

def wealth(b):
    return (1+b)/2*(2-b)

def universality_factor(n):
    reciprocal=sum(F(comb(n,k))*F(k,n)**k*F(n-k,n)**(n-k) for k in range(n+1))
    return 1/reciprocal

def run(output_dir):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['svg.hashsalt']='information-theory-ch16-portfolio-v1'
    b=[i/400 for i in range(401)]
    y=[wealth(t) for t in b]
    fig,ax=plt.subplots(figsize=(7.4,4.5),layout='constrained')
    ax.plot(b,y,color='#205b96',lw=2.3,label=r'$S_2(b)=1+b/2-b^2/2$')
    ax.scatter([0,.5,1],[1,9/8,1],color='#205b96',zorder=4)
    ax.annotate('Maximum: 9/8 at b = 1/2',xy=(.5,9/8),xytext=(.5,1.14),ha='center',fontsize=10)
    ax.axhline(13/12,color='#be6126',ls='--',lw=1.6,label=r'Uniform-portfolio average: $13/12$')
    ax.set(xlim=(0,1),ylim=(.985,1.155),xlabel='Fraction b allocated to the first (cash) asset',ylabel='Two-day wealth factor',title='Exercise 16.9: constant-rebalanced wealth')
    ax.grid(alpha=.2);ax.legend(loc='lower center',fontsize=9)
    paths=[]
    for name in ['wealth.svg','wealth.png']:
        path=output_dir/name
        metadata={'Date':None} if name.endswith('.svg') else {'Software':'information-theory-solutions'}
        fig.savefig(path,dpi=170,metadata=metadata)
        paths.append(path.relative_to(output_dir.parents[2]).as_posix())
    plt.close(fig)
    values=[universality_factor(n) for n in [1,2,3]]
    b2=F(5,12)/F(3,4); reverse=F(2,3)/F(3,2)
    checks={
        'wealth_maximum_exact':wealth(F(1,2))==F(9,8),
        'universal_rebalancing_identity':F(3,4)*(b2+2*(1-b2))==F(13,12),
        'reversal_rebalancing_identity':F(3,2)*(reverse+(1-reverse)/2)==F(13,12),
        'wealth_endpoint_values':wealth(F(0))==wealth(F(1))==1,
        'universality_factors_exact':values==[F(1,2),F(2,5),F(9,26)],
        'growth_optimum_samples':all(max(.5*log2((c+(1-c)*a)*(c+(1-c)/a)) for c in b)<=log2((a+1)/(2*a**.5))+1e-12 for a in [2,4,16]),
        'short_sale_identity_samples':all(isclose(p*log2(3*p)+(1-p)*log2(1.5*(1-p)),log2(3)-(1-p)+p*log2(p)+(1-p)*log2(1-p),abs_tol=1e-14) for p in [.1,.2,.5,.8,.9]),
    }
    return {'results':{'16.9':{'maximum_wealth':str(F(9,8)),'maximizer':str(F(1,2)),'universal_wealth':str(F(13,12)),'first_portfolio_cash':str(F(1,2)),'second_portfolio_cash':str(b2),'second_portfolio_cash_reversed':str(reverse)},
                       '16.11':{str(n):{'exact':str(v),'decimal':float(v)} for n,v in zip([1,2,3],values)}},
            'checks':checks,'seed':0,'dependencies':['matplotlib'],'source_files':[],'artifacts':paths}
