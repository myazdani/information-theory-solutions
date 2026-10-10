"""Exact exponential-bin entropy and the fine-quantization approximation."""
import math

def run(output_dir):
    rate=math.log(2)/80; delta=0.001; u=rate*delta
    exact=-math.log2(-math.expm1(-u))+u/(math.log(2)*math.expm1(u))
    approx=math.log2(math.e/(rate*delta))
    return {'seed':0,'results':{'rate_per_year':rate,'resolution_years':delta,'exact_bits':exact,'approximate_bits':approx},'checks':{'approximation_error_below_1e-9':abs(exact-approx)<1e-9,'median_verified':abs(math.exp(-rate*80)-0.5)<1e-14},'source_files':[]}
