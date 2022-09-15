#Our problem is group testing under dependent variables
#some data profiles are dependent and partitioning one affects other profiles also!
#We need smarter ways to perform group testing to partition the dataset!


'''
This file identifies the different data profiles we consider
'''
import random
import nltk,math
import pandas as pd
import argparse
import csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from sklearn.metrics import precision_recall_fscore_support
from scipy.stats import pearsonr
from sklearn.metrics import confusion_matrix
import prose.datainsights as di

class Dataset:
	profile_lst=[]
	def __init__(self,df):
		self.df=df
	def get_type(self,lst,typeval):
		uniqval=list(set(lst))
		if not 'float' in typeval and not 'int' in typeval and len(uniqval) < len(lst)/2:
			return "categorical"
		else:
			return typeval
	def populate_profiles(self):
		column_types=self.df.dtypes
		numerical_columns=[]
		categorical_columns=[]
		profile_map={}
		P=Profile()
		for column in self.df.columns:
			#print (column_types[column])
			typ=self.get_type(list(self.df[column]),str(column_types[column]))
			print (typ)
			if 'float' in typ or 'int' in typ:
				numerical_columns.append(column)
				profiles=P.get_numerical_singular_profiles(self.df[column])
				for profile in profiles:
					profile_map[(profile,column)]=profiles[profile]
				#print (profile_map)
			elif 'categorical' in typ:
				categorical_columns.append(column)
				profiles=P.get_categorical_singular_profiles(self.df[column])
				for profile in profiles:
					profile_map[(profile,column)]=profiles[profile]
			else:
				profiles=P.get_text_singular_profiles(self.df[column])
				for profile in profiles:
					profile_map[(profile,column)]=profiles[profile]
				#profile_map[column]=P.get_text_singular_profiles(self.df[column])

		i=0
		while i<len(numerical_columns):
			j=i+1
			if numerical_columns[i]=='Diverted':
				i+=1
				continue
			while j<len(numerical_columns):
				if numerical_columns[j]=='Diverted':
					j+=1
					continue
				print (numerical_columns[i],numerical_columns[j])

				profile_map[("corr",numerical_columns[i],numerical_columns[j])]=P.correlation(self.df[numerical_columns[i]],self.df[numerical_columns[j]])
				print   (profile_map[("corr",numerical_columns[i],numerical_columns[j])])
				j+=1
			i+=1
		assertions = di.learn_assertions(self.df, max_self_violation=1)
		profile_map["conformance"]=assertions
		return (profile_map)

class Profile:
	#Considers a list of data profiles for singular columns and pairs of columns

	def __init__(self):
		self.profile_lst=[]

		self.numerical_singular_profiles={'min':self.identify_min_profile,'max':self.identify_max_profile,
		'uniq':self.fraction_unique_values}#,'outlier':self.get_outlier}#,'domain':self.domain}

		self.categorical_singular_profiles={'domain':self.domain}#,'domain':self.domain}

		self.text_singular_profiles={'length':self.text_length}
		self.numerical_pairwise_profiles={'corr':self.correlation}
		self.numerical_pair={'correlation':self.correlation}
	def add_profile(self,profile):
		self.profile_lst.append(profile)
	def get_text_singular_profiles(self,lst):
		profile_dic={}
		for profile_type in self.text_singular_profiles.keys():
			profile_dic[profile_type] = self.text_singular_profiles[profile_type](lst)
		return profile_dic
	def get_categorical_singular_profiles(self,lst):
		profile_dic={}
		for profile_type in self.categorical_singular_profiles.keys():
			profile_dic[profile_type] = self.categorical_singular_profiles[profile_type](lst)
		return profile_dic

	def get_numerical_singular_profiles(self,lst):
		profile_dic={}
		for profile_type in self.numerical_singular_profiles.keys():
			profile_dic[profile_type] = self.numerical_singular_profiles[profile_type](lst)
		return profile_dic
	def get_outlier(self,lst):
		
		return 
	def identify_min_profile(self,lst):
		return min(lst)

	def identify_max_profile(self,lst):
		return max(lst)

	def fraction_unique_values(self,lst):
		return len(list(set(lst)))*1.0/len(lst)

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
		return pearsonr(lst1,lst2)[0]
		if pearsonr(lst1,lst2)[0]<0.2 and pearsonr(lst1,lst2)[0]>-0.2:
			return 0
		else:
			return 1


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
		random.shuffle(lst)
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
