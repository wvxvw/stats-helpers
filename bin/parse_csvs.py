#!/usr/bin/env python

import pandas as pd
import os
import math


def choose_or_avg(a, b):
    if type(a) is str:
        a = float(a)
    if type(b) is str:
        b = float(b)
    if math.isnan(a) and math.isnan(b):
        return math.nan
    if math.isnan(a):
        return b
    if math.isnan(b):
        return a
    return (a + b) / 2


def partition_tp_tn_fp_fn(a, b):
    if a and b:
        return 'tp'
    if a and not b:
        return 'fn'
    if not a and b:
        return 'fp'
    return 'tn'


def process_csv(df):
    df = df[10:19]
    columns = list(df.ix[:, 0])
    rest = df.ix[:, 1:]
    dft = rest.transpose()
    dft.columns = columns
    dft['invasive blood sugar combined'] = dft['1. invasive blood sugar, CoG'].combine(
        dft['2. invasive blood sugar, CoG'],
        choose_or_avg,
    )
    filtered = pd.DataFrame(dft['invasive blood sugar combined'])
    # filtered.rename(columns={'invasive blood sugar combined': 'invasive'}, inplace=True)
    filtered['noninvasive'] = dft['Non-invasive blood sugar, CoG']
    filtered['noninvasive'] = filtered['noninvasive'].astype(float)
    filtered.dropna(inplace=True)
    filtered['threshold1'] = filtered['invasive blood sugar combined'] > 120
    filtered['threshold2'] = filtered['noninvasive'] > 120
    filtered['partitioned'] = filtered['threshold1'].combine(
        filtered['threshold2'],
        partition_tp_tn_fp_fn,
    )
    numerator = filtered['threshold1'].sum()
    denominator = (filtered['partitioned'] == 'tn').sum()
    print(numerator / denominator)
    
    import pdb
    pdb.set_trace()

for file in os.listdir('csv'):
    process_csv(pd.read_csv(os.path.join('csv', file)))
