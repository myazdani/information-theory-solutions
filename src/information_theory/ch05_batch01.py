"""Exact D-ary Huffman constructions for Chapter 5, first group."""
from fractions import Fraction
import heapq
from math import log2,isclose
from .numerics import entropy

def huffman(weights,radix=2):
    weights=[Fraction(w) for w in weights];m=len(weights)
    pad=(1-m)%(radix-1);heap=[];serial=0;merges=[]
    for i,w in enumerate(weights+[Fraction(0)]*pad):
        heapq.heappush(heap,(w,serial,i));serial+=1
    while len(heap)>1:
        children=[heapq.heappop(heap) for _ in range(radix)]
        total=sum(x[0] for x in children);merges.append([str(x[0]) for x in children])
        heapq.heappush(heap,(total,serial,tuple(x[2] for x in children)));serial+=1
    codes={}
    def walk(node,s):
        if isinstance(node,int):
            if node<m:codes[node]=s
        else:
            for i,child in enumerate(node):walk(child,s+str(i))
    walk(heap[0][2],'');ordered=[codes[i] for i in range(m)];total=sum(weights)
    mean=sum(w*len(c) for w,c in zip(weights,ordered))/total
    kraft=sum(Fraction(1,radix**len(c)) for c in ordered)
    return {'codes':ordered,'lengths':list(map(len,ordered)),'average_length':float(mean),'average_length_exact':str(mean),'kraft':float(kraft),'merges':merges,'dummy_leaves':pad}

def run(output_dir):
    cases={'5.4.binary':([49,26,12,4,4,3,2],2),'5.4.ternary':([49,26,12,4,4,3,2],3),'5.5':([5,3,3,2,2],2),'5.12':([4,4,3,1],2),'5.14.binary':([1,2,3,4,5,6],2),'5.14.ternary':([1,2,3,4,5,6],3),'5.15':([3,3,2,1,1],2),'5.16.binary':([10,5,2,1,1,1],2),'5.16.quaternary':([10,5,2,1,1,1],4),'5.17.a':([10,9,8,7,7],2)}
    results={name:huffman(w,d) for name,(w,d) in cases.items()};checks={}
    for name,(w,radix) in cases.items():
        z=results[name];codes=z['codes'];p=[x/sum(w) for x in w]
        checks[name+'_prefix_free']=all(not b.startswith(a) for i,a in enumerate(codes) for j,b in enumerate(codes) if i!=j)
        checks[name+'_entropy_bound']=entropy(p)/log2(radix)-1e-12<=z['average_length']<entropy(p)/log2(radix)+1+1e-12
    results['5.8']={'stationary':[2/9,4/9,1/3],'conditional_lengths':[1.5,1.5,1.],'rate':4/3}
    pi=results['5.8']['stationary'];P=[[.5,.25,.25],[.25,.5,.25],[0,.5,.5]]
    checks['5.8_stationary']=all(isclose(sum(pi[i]*P[i][j] for i in range(3)),pi[j]) for j in range(3))
    checks['5.8_rate']=isclose(sum(p*entropy(row) for p,row in zip(pi,P)),4/3)
    return {'seed':0,'dependencies':[],'results':results,'checks':checks,'source_files':['src/information_theory/numerics.py']}
