#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup


project_dir = os.path.dirname(os.path.realpath(__file__))
sys.path = [x for x in sys.path if not x == project_dir]


setup(
    packages=['cnoga_stats'],
    name='conga-stats',
    version='0.0.1',
    description='Script helpers to process some stats',
    author=[
        'Makeda Moore',
        'Oleg Sivokon',
    ],
    author_email=[
        # Put Makeda's email here
        'oleg.sivokon@replixio.com',
    ],
    url='TBD',
    scripts=[
        'bin/parse_csvs.py',
        'bin/xls2csv.py',
        'bin/compare_swatches.py',
        'bin/calibration-pattern.py',
    ],
    license='PROPRIETARY',
    install_requires=[
        'pandas >= 0.24.2',
        'xlrd >= 1.2.0',
        'Pillow >= 6.0.0',
        'matplotlib >= 3.1.1',
    ],
)
