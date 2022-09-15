#import blink.main_dense as main_dense
import argparse

import spacy

def get_runtime(df):

    if df.shape[0]<10000:
        return 1#Pass
    else:
        return 0#Fail
