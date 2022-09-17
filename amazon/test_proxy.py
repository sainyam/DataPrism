#import blink.main_dense as main_dense
import argparse

import spacy

def get_runtime(df):
    print(df)
    print(df.dtypes)
    print (df['text'].astype(str).apply(len).mean())

    if df['text'].astype(str).apply(len).mean()<140 and  df.shape[0]<10000:
        return 1#Pass
    elif df.shape[0]<10000:
        return 0.5
    else:
        return 0#Fail
