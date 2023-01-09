'''
This pipeline assumes that the tweet length is 140 characters. 
'''

import nltk
import pandas as pd

import argparse
import csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from sklearn.metrics import precision_recall_fscore_support

from textblob import TextBlob

import flair

from sklearn.metrics import confusion_matrix

nltk.download('vader_lexicon')

def compute_sentiment(tweet_df):
	#tweet_df= pd.read_csv(filepath,encoding="ISO-8859-1")

	analyzer = SentimentIntensityAnalyzer()
	flair_sentiment = flair.models.TextClassifier.load('en-sentiment')
	prediction_lst=[]
	true_val=[]

	num_rows_considered=100
	#print (tweet_df['target'].values)
	tweet_df=tweet_df.sample(frac=0.01)

	for index,row in tweet_df.iterrows():
		tweet_text=row['text']#[:140]
		#print (tweet_text,len(tweet_text))
		if len(prediction_lst)>=num_rows_considered:
			break
		if index%10000==0:
			print(index)
		option=2
		prediction=-100
		if option==1:
			scores= analyzer.polarity_scores(tweet_text)
			score_lst=[scores['neg'],scores['neu'],scores['pos']]
			prediction= (score_lst.index(max(score_lst))-1)
		elif option==2:
			flair_sent = flair.data.Sentence(tweet_text)
			flair_sentiment.predict(flair_sent)
			sentiment_pred = flair_sent.labels[0].to_dict()
			#print(sentiment_pred,row['target'],tweet_text)
			if 'NEGATIVE' in sentiment_pred['value']:
				prediction=-1
			elif 'POSITIVE' in sentiment_pred['value']:
				prediction=1
			else:
				prediction=0
		else:
			sentiment_pred=TextBlob(row['text']).sentiment.polarity
			if sentiment_pred>0.5:
				prediction=1
			elif sentiment_pred<-0.5:
				prediction=-1
			else:
				prediction=0
		prediction_lst.append(prediction)
		true_val.append(row['target'])
	#print (prediction_lst,true_val)
	print (confusion_matrix(true_val,prediction_lst))
	score = precision_recall_fscore_support(true_val,prediction_lst, average='micro')
	print (score)
	return score[0] #> threshold


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, help="path to the input file containing tweets")
    args = parser.parse_args()

    compute_sentiment(pd.read_csv(args.data,encoding="ISO-8859-1"))
