
import nltk
import pandas as pd

import argparse
import csv


def process_dataframe(filepath,output_file):
	tweet_df= pd.read_csv(filepath,encoding="ISO-8859-1",names=['target','id','date','flag','user','text'])

	tweet_df['target'] = (tweet_df['target']-2)/2

	tweet_df.to_csv(output_file,index=False,quoting=csv.QUOTE_ALL)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, help="path to the input file containing tweets")
    parser.add_argument("--output", type=str, help="path to the output file")
    args = parser.parse_args()

    process_dataframe(args.data,args.output)