#!/usr/bin/env python

import pandas as pd
import os

from argparse import ArgumentParser


parser = ArgumentParser(
    '''
    Converts a list of directories containing MS Excel files into CSV files
    '''
)
parser.add_argument(
    'xls',
    nargs='+',
    help='Directories containing MS Excel files',
)
parser.add_argument(
    '-o',
    '--output',
    default='.',
    help='Where should the resulting CSV be stored',
)

args = parser.parse_args()
for d in args.xls:
    for f in os.listdir(d):
        with open(os.path.join(d, f), 'br') as s:
            res = pd.read_excel(f, sheet_name=None)
            if not type(res) is dict:
                res = {'': res}
            for k, v in res.itmes():
                csv = '{}-{}.csv'.format(f, k)
                v.to_csv(os.path.join(args.output, csv))
