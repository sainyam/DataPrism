'''
This pipeline considers synthetic error.

'''

import pandas as pd

import argparse
import csv

from sklearn.metrics import precision_recall_fscore_support


def run_pipeline(df, bugs):

    violation = 0
    for index, row in df.isnull().iterrows():
        if any([all([row.iloc[int(c)] for c in bug]) for bug in bugs]):
            violation += 1
    return violation


def run(data, threshold, bugs):
    df = pd.read_csv(data)
    violation = run_pipeline(df, bugs)
    return violation < int(threshold), violation
