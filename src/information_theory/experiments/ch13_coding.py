"""Exact arithmetic coding and dictionary checks for Chapter 13."""
from fractions import Fraction as F
from itertools import product
from math import log2, ceil

def interval(bits, stay):
    lo, hi = F(0), F(1)
    previous = None
    for char in bits:
        pzero = F(1, 2) if previous is None else (stay if previous == '0' else 1-stay)
        split = lo + (hi-lo)*pzero
        lo, hi = (lo, split) if char == '0' else (split, hi)
        previous = char
    return lo, hi

def common_bits(lo, hi, limit=128):
    answer = ''
    for _ in range(limit):
        lo *= 2; hi *= 2
        bit = int(lo)
        if hi > bit+1:
            break
        answer += str(bit)
        lo -= bit; hi -= bit
    return answer

def lz78(text):
    dictionary = {'': 0}; phrases=[]; pairs=[]; position=0
    while position < len(text):
        word=''
        while position < len(text) and word+text[position] in dictionary:
            word += text[position]; position += 1
        if position == len(text):
            phrases.append(word); pairs.append([dictionary[word], None]); break
        char=text[position]; position += 1
        phrases.append(word+char); pairs.append([dictionary[word], char])
        dictionary[word+char]=len(dictionary)
    return phrases, pairs

def decode(pairs):
    dictionary=['']; result=''
    for index,char in pairs:
        word=dictionary[index]+(char or '')
        result+=word
        if char is not None: dictionary.append(word)
    return result

def run(output_dir):
    first=interval('1010111', F(3,4))
    second=interval('01110', F(1,3))
    cell=(F(4,8),F(5,8))
    candidates=[''.join(w) for w in product('01',repeat=5) if interval(''.join(w),F(3,4))[0]<cell[1] and interval(''.join(w),F(3,4))[1]>cell[0]]
    common=candidates[0]
    for word in candidates:
        while not word.startswith(common): common=common[:-1]
    texts=['00000011010100000110101','0'+'00'+'001'+'00000011010111']
    parses=[lz78(t) for t in texts]
    entropy=-sum(p*log2(p) for p in [.7,.2,.1])
    checks={
        'arithmetic_first_prefix':common_bits(*first).startswith('100'),
        'arithmetic_second_lower':second[0]==F(25,54),
        'arithmetic_second_upper':second[1]==F(79,162),
        'lz_roundtrips':all(decode(p[1])==t for p,t in zip(parses,texts)),
        'arithmetic_partition':sum(interval(''.join(w),F(3,4))[1]-interval(''.join(w),F(3,4))[0] for w in product('01',repeat=7))==1,
        'lz77_threshold':1+12+8 < 9*3 and 1+12+8 > 9*2,
    }
    return {'results':{
        '13.2':{'entropy_bits':entropy,'minimax_bits':log2(3)-entropy,'ideal_length_bits':log2(3)},
        '13.3':{'interval':[str(v) for v in first],'known_code_bits':common_bits(*first),'decoded_from_100':common,'intersecting_length_5_prefixes':candidates},
        '13.4':{'interval':[str(v) for v in second],'known_code_bits':common_bits(*second)},
        '13.5':{'phrases':parses[0][0],'pairs':parses[0][1]},
        '13.8':{'pointer_bits':12,'length_bits':8,'shortest_strictly_better_match':3},
        '13.9':{'phrases':parses[1][0],'pairs':parses[1][1]},
    },'checks':checks,'seed':0,'dependencies':[],'source_files':[]}
