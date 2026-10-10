"""Constraint growth and exact finite-graph entropy rates."""
from math import log2,isclose
from itertools import combinations,product
from collections import Counter
from .numerics import entropy,binary_entropy

def graph_stats(vertices,edges):
    adj={v:set() for v in vertices}
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    degree=[len(adj[v]) for v in vertices];total=sum(degree)
    pi=[d/total for d in degree]
    h=sum(p*log2(d) for p,d in zip(pi,degree) if d)
    return {'degrees':degree,'stationary':pi,'rate':h,'state_entropy':entropy(pi),'mutual_information':entropy(pi)-h}

def run(output_dir):
    lo,hi=1.,2.
    for _ in range(100):
        mid=(lo+hi)/2
        if mid**3-mid-1<0:lo=mid
        else:hi=mid
    lam=(lo+hi)/2;alpha=lam**-2;stationary=[1/(3-alpha),1/(3-alpha),(1-alpha)/(3-alpha)]
    g19=graph_stats(list(range(1,6)),[(1,2),(1,5),(1,4),(2,3),(2,5),(3,5),(3,4),(4,5)])
    board=list(product(range(3),repeat=2));pairs=list(combinations(board,2));chess={}
    for piece in ['king','rook','bishop_even','bishop_odd','queen']:
        vs=[v for v in board if not piece.startswith('bishop') or sum(v)%2==(0 if piece.endswith('even') else 1)]
        edges=[]
        for a,b in combinations(vs,2):
            dx,dy=abs(a[0]-b[0]),abs(a[1]-b[1]);rook=dx==0 or dy==0;bishop=dx==dy
            legal=max(dx,dy)==1 if piece=='king' else rook if piece=='rook' else bishop if piece.startswith('bishop') else rook or bishop
            if legal:edges.append((a,b))
        chess[piece]=graph_stats(vs,edges)
    extrema=[]
    for n in [4,5]:
        for edges in combinations(list(combinations(range(n),2)),4):
            reached={0}
            while True:
                new=reached|{b for a,b in edges if a in reached}|{a for a,b in edges if b in reached}
                if new==reached:break
                reached=new
            if len(reached)==n:
                g=graph_stats(list(range(n)),edges);extrema.append((g['rate'],sorted(g['degrees'],reverse=True)))
    cube=list(product(range(3),repeat=3));maze=graph_stats(cube,[(a,b) for a,b in combinations(cube,2) if sum(abs(x-y) for x,y in zip(a,b))==1])
    count=[1,1,0]
    for _ in range(1,1000):count=[count[1]+count[2],count[0],count[1]]
    growth=log2(sum(count))/1000
    results={'constraint_lambda':lam,'constraint_alpha':alpha,'constraint_stationary':stationary,'constraint_max_rate':binary_entropy(alpha)/(3-alpha),'constraint_log2_lambda':log2(lam),'constraint_count_rate_at_n1000':growth,'graph_4_19':g19,'chess':chess,'four_edge_graph_min':min(extrema),'four_edge_graph_max':max(extrema),'four_edge_degree_sequences':sorted({tuple(d) for _,d in extrema}),'maze_degree_counts':dict(Counter(maze['degrees'])),'maze_rate':maze['rate']}
    checks={'cubic_root':abs(lam**3-lam-1)<1e-14,'alpha_maximizer_equation':abs((1-alpha)**2-alpha**3)<1e-14,'constraint_rate_equals_growth':isclose(binary_entropy(alpha)/(3-alpha),log2(lam),abs_tol=1e-14),'count_rate_converges':abs(growth-log2(lam))<.002,'graph_degrees':g19['degrees']==[3,3,3,3,4],'rook_two_bits':isclose(chess['rook']['rate'],2),'bishop_rates':isclose(chess['bishop_even']['rate'],4/3) and isclose(chess['bishop_odd']['rate'],1),'extremal_graphs':min(extrema)[1]==[2,2,2,1,1] and max(extrema)[1]==[3,2,2,1],'maze_total_degree':sum(maze['degrees'])==108}
    return {'seed':0,'dependencies':[],'results':results,'checks':checks,'source_files':['src/information_theory/numerics.py']}
