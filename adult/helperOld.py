#Our problem is group testing under dependent variables
#some data profiles are dependent and partitioning one affects other profiles also!
#We need smarter ways to perform group testing to partition the dataset!


'''
This file identifies the different data profiles we consider
'''
import random
import nltk,math
import pandas as pd
import numpy as np
import argparse
import csv,collections
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from sklearn.metrics import precision_recall_fscore_support
from scipy.stats import pearsonr
from sklearn.metrics import confusion_matrix
import statistics 
import prose.datainsights as di
from scipy.stats import chisquare,chi2_contingency
from scipy import stats
from tdda.rexpy import pdextract

class Dataset:
	profile_lst=[]
	def __init__(self,df):
		self.df=df

	def populate_profiles(self):
		column_types=self.df.dtypes
		numerical_columns=[]
		categorical_columns=[]
		profile_map={}
		P=Profile()

		for column in self.df.columns:
			#print (column_types[column])
			values=list(self.df[column].values)
			uniq_values=list(set(values))
			if len(uniq_values) < 10 and len(values)>2*len(uniq_values):#Check if a column is categorical
				print("categorical column",column)
				categorical_columns.append(column)
				profiles=P.get_categorical_singular_profiles(self.df[column])
				for profile in profiles:
					profile_map[(profile,column)]=profiles[profile]
			elif 'float' in str(column_types[column]) or 'int' in str(column_types[column]):
				numerical_columns.append(column)
				profiles=P.get_numerical_singular_profiles(self.df[column])
				for profile in profiles:
					profile_map[(profile,column)]=profiles[profile]
				#print (profile_map)
			else:
				profiles=P.get_text_singular_profiles(self.df[column])
				for profile in profiles:
					profile_map[(profile,column)]=profiles[profile]
				#profile_map[column]=P.get_text_singular_profiles(self.df[column])

		i=0
		while i<len(numerical_columns):
			j=i+1
			while j<len(numerical_columns):
				#print (numerical_columns[i],numerical_columns[j])
				profile_map[("corr",numerical_columns[i],numerical_columns[j])]=P.correlation(self.df[numerical_columns[i]],self.df[numerical_columns[j]])
				j+=1
			i+=1

		i=0
		while i<len(categorical_columns):
			j=i+1
			while j<len(categorical_columns):
				#print (numerical_columns[i],numerical_columns[j])
				profile_map[("corr",categorical_columns[i],categorical_columns[j])]=P.categorical_correlation(self.df[categorical_columns[i]],self.df[categorical_columns[j]])
				j+=1
			i+=1

		i=0
		while i<len(numerical_columns):
			j=0
			while j<len(categorical_columns):
				profile_map[("corr",numerical_columns[i],categorical_columns[j])]=P.categorical_numerical_correlation(self.df[numerical_columns[i]],self.df[categorical_columns[j]])
				
				#print (numerical_columns[i],categorical_columns[j],stats.f_oneway(self.df[numerical_columns[i]], self.df[categorical_columns[j]]))
				#profile_map[("corr",categorical_columns[i],categorical_columns[j])]=P.categorical_correlation(self.df[categorical_columns[i]],self.df[categorical_columns[j]])
				j+=1
			i+=1

		plst=['conformance']
		plst.extend(numerical_columns)
		assertions = di.learn_assertions(self.df[numerical_columns], max_self_violation=1)
		profile_map[tuple(plst)]=assertions

		p2lst=['dataset_size']
		p2lst.extend(list(self.df.columns))
		profile_map[tuple(p2lst)]=self.df.shape[0]


		return (profile_map)

class Profile:
	#Considers a list of data profiles for singular columns and pairs of columns

	def __init__(self):
		self.profile_lst=[]

		self.numerical_singular_profiles={'min':self.identify_min_profile,'max':self.identify_max_profile,
		'uniq':self.fraction_unique_values,'outlier':self.outlier,'missing':self.missing}#,'domain':self.domain}
		self.categorical_singular_profiles={'min':self.identify_min_profile,'max':self.identify_max_profile,
		'uniq':self.fraction_unique_values,'outlier':self.outlier_distribution,'missing':self.missing,'domain':self.identify_domain_profile}
		self.text_singular_profiles={'length':self.text_length,'missing':self.missing,'domain':self.get_regular_exp}
		self.numerical_pairwise_profiles={'corr':self.correlation}
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
	def get_categorical_singular_profiles(self,lst):
		profile_dic={}
		for profile_type in self.categorical_singular_profiles.keys():
			profile_dic[profile_type] = self.categorical_singular_profiles[profile_type](lst)
		return profile_dic

	def identify_min_profile(self,lst):
		return min(lst)

	def identify_max_profile(self,lst):
		return max(lst)

	def identify_domain_profile(self,lst):
		return list(set(lst))

	def fraction_unique_values(self,lst):
		return len(list(set(lst)))*1.0/len(lst)

	def outlier(self,lst):
		mean=statistics.mean(lst)
		std=statistics.stdev(lst)
		count=0
		for v in lst:
			if v>mean+2*std or v<mean-2*std:
				count+=1
		return count*1.0/len(lst)
	def get_regular_exp(self,lst):
		return pdextract(lst)
	def outlier_distribution(self,lst):
		counts=collections.Counter(lst)

		mean=statistics.mean(counts.values())
		std=statistics.stdev(counts.values())

		outliers=[]
		count=0
		for v in counts.keys():
			if counts[v]>mean+2*std or counts[v]<mean-2*std:
				outliers.append(v)
		
		for v in lst:
			if v in outliers:
				count+=1
		return count*1.0/len(lst)

	def numerical_selectivity(self,lst,pred):
		#pred is a list of pairs (lb,ub)
		count=0
		for v in lst:
			for (lb,ub) in pred:
				if v<=ub and v>=lb:
					count+=1
					break
		return count*1.0/len(lst)

	def missing (self,lst):
		count=0
		for v in lst:
			if np.isnan(v):
				count+=1
		return count*1.0/len(lst)

	def domain(self,lst):
		return (list(set(lst)))

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
		(r,p)= pearsonr(lst1,lst2)
		if p<0.05:
			return r
		else:
			return 0

	def categorical_correlation(self,lst1,lst2):
		cross_tab=pd.crosstab(lst1,lst2)
		chi2, p, dof, ex=chi2_contingency(cross_tab)
		if p<0.05:
			return chi2
		else:
			return 0

	def categorical_numerical_correlation(self,lst1,lst2):
		(chi2,p)=stats.f_oneway(lst1,lst2)
		if p<0.05:
			return chi2
		else:
			print ("0 correlation")
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

	def shuffle_transform(self,lst):
		print(lst)
		random.shuffle(lst)
		print('shuffle')
		return lst


if __name__ == "__main__":
    print ("this file contains a list of data profiles")
    p=Profile()
    p.add_profile(p.identify_min_profile)

    df=pd.read_csv('./Examples/tweets/sentiment140/cleaned_tweets.csv')

    df=df[['target','text']]

    #print (df)
    clean1=Dataset(df)
    print ("Clean profiles",clean1.populate_profiles())
    df=pd.read_csv('./Examples/tweets/imdb/imdb_data.csv',encoding="ISO-8859-1")
    df=df[['target','text']]

    bug1=Dataset(df)
    print ("Buggy profiles",bug1.populate_profiles())
    '''
    print (p.range(df['target']))
    print(p.correlation(df['target'],df['id']))
    print (df.dtypes)

    fail_df=pd.read_csv('./Examples/tweets/sentiment140/sentiment140.csv',encoding="ISO-8859-1")
    print (fail_df)
    print(p.correlation(fail_df['target'],fail_df['id']))
	'''
