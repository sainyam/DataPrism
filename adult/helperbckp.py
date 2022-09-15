#Our problem is group testing under dependent variables
#some data profiles are dependent and partitioning one affects other profiles also!
#We need smarter ways to perform group testing to partition the dataset!


'''
This file identifies the different data profiles we consider
'''

import nltk,math
import pandas as pd
import argparse
import csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from sklearn.metrics import precision_recall_fscore_support
from scipy.stats import pearsonr
from sklearn.metrics import confusion_matrix
class dataset:
	profile_lst=[]
	def __init__(self,df):
		self.df=df

	def populate_profiles(self):
		column_types=self.df.dtypes
		numerical_columns=[]
		profile_map={}
		P=Profile()
		for column in df.columns:
			print (column_types[column])
			if 'float' in str(column_types[column]) or 'int' in str(column_types[column]):
				numerical_columns.append(column)
				profile_map[column]=P.get_numerical_singular_profiles(df[column])
			else:
				profile_map[column]=P.get_text_singular_profiles(df[column])
		return (profile_map)

class Profile:
	#Considers a list of data profiles for singular columns and pairs of columns

	def __init__(self):
		self.profile_lst=[]

		self.numerical_singular_profiles={'min':self.identify_min_profile,'max':self.identify_max_profile,
		'uniq':self.fraction_unique_values,'domain':self.domain}

		self.text_singular_profiles={'length':self.text_length}

		self.numerical_pair={'correlation':self.correlation}
	def add_profile(self,profile):
		self.profile_lst.append(profile)
	def get_text_singular_profiles(self,lst):
		profile_dic={}
		for profile_type in self.text_singular_profiles.keys():
			profile_dic[profile_type] = self.text_singular_profiles[profile_type](lst)
		return profile_dic
	def get_numerical_singular_profiles(self,lst):
		profile_dic={}
		for profile_type in self.numerical_singular_profiles.keys():
			profile_dic[profile_type] = self.numerical_singular_profiles[profile_type](lst)
		return profile_dic

	def identify_min_profile(self,lst):
		return min(lst)

	def identify_max_profile(self,lst):
		return max(lst)

	def fraction_unique_values(self,lst):
		return len(list(set(lst)))*1.0/len(lst)

	def domain(self,lst):
		return (list(set(lst)))

	def fraction_occurence(self,lst,val):
		count=0
		for v in lst:
			if v==val:# or lower(v)==val:
				count+=1
		return count*1.0/len(lst)
	def range(self,lst):
		return (self.identify_min_profile(lst),self.identify_max_profile(lst))

	def text_length(self,lst):
		size_lst=[]
		for row in lst:
			#if len(row)>240:
			#	print (row,len(row))
			size_lst.append(len(row))
		return (self.identify_max_profile(size_lst),self.identify_min_profile(size_lst),self.fraction_unique_values(size_lst))

	def correlation(self,lst1,lst2):
		corr=pearsonr(lst1,lst2)[0]
		if corr>0.2:
			return corr
		else:
			return 0


	def histogram(self,lst):
		count_dic={}
		for val in lst:
			if val in count_dic.keys():
				count_dic[va]=count_dic[val]+1
			else:
				count_dic[val]=1
		return (count_dic)


	def linear_transform(self,lst,addition,multiplication):
		new_lst=[]
		for v in lst:
			new_lst.append(v*multiplication+addition)
		return new_lst


if __name__ == "__main__":
    print ("this file contains a list of data profiles")
    p=Profile()
    p.add_profile(p.identify_min_profile)

    df=pd.read_csv('./Examples/tweets/stanfordSentimentTreebank/cleaned_tweets.csv')

    df=df[['target','text']]

    #print (df)
    clean1=dataset(df)
    print ("Clean profiles",clean1.populate_profiles())
    df=pd.read_csv('./Examples/tweets/sentiment140/sentiment140.csv',encoding="ISO-8859-1")
    df=df[['target','text']]

    bug1=dataset(df)
    print ("Buggy profiles",bug1.populate_profiles())
    



    df=pd.read_csv('./data/adult/train.txt',delimiter=' ')
    feat=list(df.columns)
    feat.remove('Unnamed: 15')
    print (df,feat)
    i=0
    while i<len(feat):
    	j=i+1
    	while j<len(feat):
    		print (feat[i],feat[j],p.correlation(df[feat[i]],df[feat[j]]))
    		j+=1
    	i+=1

    sample=df[df['sex']==0]
    sample2=df[df['sex']==1]
    print (p.fraction_occurence(sample['target'],1),p.fraction_occurence(sample2['target'],1))
    '''
    print (p.range(df['target']))
    print(p.correlation(df['target'],df['id']))
    print (df.dtypes)

    fail_df=pd.read_csv('./Examples/tweets/sentiment140/sentiment140.csv',encoding="ISO-8859-1")
    print (fail_df)
    print(p.correlation(fail_df['target'],fail_df['id']))
	'''
