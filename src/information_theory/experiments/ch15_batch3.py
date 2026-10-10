"""Frozen deterministic rate-region sketches for Exercises 15.21 and 15.23."""
from math import log2
from pathlib import Path


def h(p):
    return -sum(x * log2(x) for x in (p, 1-p) if x)


def svg(title, polygon, curve, labels, width=660, height=470):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="white"/>
<polygon points="{polygon}" fill="#d6ecea"/>
<path d="M65 65V395H595" fill="none" stroke="#222" stroke-width="2"/>
<polyline points="{curve}" fill="none" stroke="#137b74" stroke-width="3"/>
<g font-family="sans-serif" font-size="18" fill="#222"><text x="65" y="32">{title}</text><text x="604" y="400">R_1</text><text x="15" y="60">R_2</text><text x="44" y="420">0</text>{labels}<text x="207" y="450">Rates in bits per use</text></g></svg>'''


def run(output_dir):
    c1, c2 = (1-.2), (1-.2)*(1-.5)
    labels='<text x="466" y="421">0.8</text><text x="21" y="125">0.4</text><text x="120" y="348">Achievable region</text>'
    path1=output_dir/'ex-15-21.svg'
    path1.write_text(svg('Cascaded erasure broadcast: alpha1=0.2, alpha2=0.5', '65,395 485,395 65,115', '485,395 65,115', labels))
    L=log2(3)
    points=[(1,0)]+[(h(.5+i/400),(.5+i/400)*L) for i in range(201)]
    coord=lambda pair:f'{65+480*pair[0]:.3f},{395-185*pair[1]:.3f}'
    curve=' '.join(map(coord,points)); polygon='65,395 '+curve
    labels='<text x="538" y="420">1</text><text x="7" y="106">1.585</text><text x="407" y="282">(1, 0.792)</text><text x="137" y="350">Achievable region</text>'
    path2=output_dir/'ex-15-23.svg'
    path2.write_text(svg('Gated ternary multiple-access capacity',polygon,curve,labels))
    values=[h(i/1000)+(i/1000)*L for i in range(1001)]
    root=Path(__file__).resolve().parents[3]
    return {'results':{'erasure_intercepts':[c1,c2],'log2_3':L,'gated_corner':[1,L/2],
                       'maximum_sum_point':[h(.75),.75*L],'maximum_sum_rate':h(.75)+.75*L,
                       'grid_maximum_sum_rate':max(values),'grid_size':1001},
            'checks':{'erasure_intercepts':abs(c1-.8)<1e-14 and abs(c2-.4)<1e-14,
                      'maximum_sum_equals_two':abs(h(.75)+.75*L-2)<1e-14,
                      'grid_sum_at_most_two':max(values)<=2+1e-14,
                      'region_endpoints':h(.5)==1 and h(1)==0},
            'source_files':[],'seed':None,'dependencies':[],
            'artifacts':[p.relative_to(root).as_posix() for p in (path1,path2)]}
