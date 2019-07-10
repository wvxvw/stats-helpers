#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import os

from argparse import ArgumentParser
from datetime import timedelta

import pandas as pd
import matplotlib.pyplot as plt

parser = ArgumentParser('Plot calibration pattern')
parser.add_argument(
    'csvs',
    nargs='+',
    help='''
    CSV files to read.
    '''
)


def plot_calibration(source):
    df = pd.read_csv(source)
    df['Ref1'] = df['Ref1'].astype(float)
    df['Ref2'] = df['Ref2'].astype(float)
    df['Idx'] = pd.to_datetime(df['Date&Time'], format='%Y-%m-%d %H:%M')
    nrows = 0

    for index, row in df.iterrows():
        ref1 = row['Ref1']
        ref2 = row['Ref2']
        if math.isnan(ref1) and math.isnan(ref2):
            nrows = index
            break
    df = df.head(nrows)
    start = df['Idx'].iloc[0]
    start = pd.Timestamp(start.date())
    end = df['Idx'].iloc[-1]
    end = pd.Timestamp(end.date() + timedelta(days=1))
    diff = int((end - start).total_seconds() / (60 * 60 * 2))
    dates = pd.date_range(start, periods=diff, freq='2H')
    ddf = dates.to_frame()
    ddf[1] = dates.shift(1)
    ddf.rename(columns={0: 'Start', 1: 'End'}, inplace=True)
    ddf = ddf.assign(Cal=0)
    ddf.reset_index(drop=True, inplace=True)

    cursor = 0
    max_search = len(df)
    cal_idx = ddf.columns.get_loc('Cal')

    for index, row in ddf.iterrows():
        start = row['Start']
        end = row['End']
        while cursor < max_search:
            record = df['Idx'].iloc[cursor]
            if start <= record < end:
                ddf.iat[index, cal_idx] += 1
                cursor += 1
            elif record >= end:
                break

    plt.tight_layout()
    plot = ddf.plot.bar(x='Start', y='Cal', figsize=(16, 4))
    x_labels = ddf['Start'].dt.strftime('%Y-%m-%d %H')
    plot.set_xticklabels(x_labels)
    src = os.path.basename(source)
    plot.legend(['Calibration of "{}"'.format(src)]);
    plot.set_xlabel('Calibration from midnight every two hours')
    fig = plot.get_figure()
    fig.subplots_adjust(bottom=0.35)
    fig.savefig(source + '.png')

args = parser.parse_args()

for s in args.csvs:
    plot_calibration(s)

