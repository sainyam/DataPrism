import pandas as pd
import numpy as np
from sklearn import preprocessing
import prose.datainsights as di
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from scipy.stats.stats import pearsonr  
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import os
import sys
np.random.seed(0)

import helper,airline
import math
import operator
import copy


def get_distance(clprofile,bugprofile):
	dist=0
	for profile in clprofile.keys():
		dist+=get_profile_distance(clprofile[profile],bugprofile[profile])

	return dist

def get_profile_distance_normalized(p1,p2):
	if max(p1,p2)==0:
		return 0
	#print (p1,p2)
	return abs(p1-p2)*1.0/max(p1,p2)
def get_profile_distance_corr(p1,p2):
	#print (p1,p2)
	return abs(p1-p2)

def get_profile_benefit_ordering(clprofile,bugprofile,bugdf,cleandf):
	benefit={}
	for profile in clprofile.keys():
		if profile=='conformance':
			benefit[profile]=0.1#clprofile["conformance"].evaluate(bugdf).avg_violation
			continue
		print(profile,clprofile[profile],bugprofile[profile])
		if 'max' in profile[0]:
			benefit[profile]=0.1#get_profile_distance_normalized(clprofile[profile],bugprofile[profile])
		else:	
			benefit[profile]=0.1#get_profile_distance_corr(clprofile[profile],bugprofile[profile])


	sorted_benefit = sorted(benefit.items(), key=operator.itemgetter(1),reverse=True)
	import random
	random.seed(0)
	random.shuffle(sorted_benefit)
	return sorted_benefit

def check_processed_profile(prof,processed):
	for (p,col) in processed:
		if p==prof:
			return True
	return False

def check_col(col,processed):
	for (p,column) in processed:
		if col==column:
			return True
	return False

#Processed is a list of tuples where first element is profile name and 2nd element is column name
def identify_column(benefit_ordering,processed):
	column_count={}
	for (prof,score) in benefit_ordering:
		if score==0:
			continue
		found=check_processed_profile(prof[0],processed)
		i=1
		while i<len(prof):
			
			if found:
				if check_col(prof[i],processed):
					i+=1
					continue

			if prof[i] in column_count:
				column_count[prof[i]]+=1#score
			else:
				column_count[prof[i]]=1#score
			i+=1
	sorted_column_score = sorted(column_count.items(), key=operator.itemgetter(1),reverse=True)
	#Get the profile corresponding to this columns
	print (sorted_column_score)
	identified_column=sorted_column_score[0][0]

	prof_count={}
	#Get the profile for this column!
	for (prof,score) in benefit_ordering:

		found=check_processed_profile(prof[0],processed)
		i=1
		while i<len(prof):
			
			if found:
				if check_col(prof[i],processed):
					i+=1
					continue
			#print (prof,score,identified_column)
			if prof[i] ==identified_column:
				if prof[0] in prof_count.keys():
					prof_count[prof[0]]+=score
				else:
					prof_count[prof[0]]=score
			
			i+=1
	sorted_profile_score = sorted(prof_count.items(), key=operator.itemgetter(1),reverse=True)
	identified_profile=sorted_profile_score[0][0]
	print(sorted_profile_score)
	return (identified_column,identified_profile)


p=helper.Profile()
p.add_profile(p.identify_min_profile)

noisydf=pd.read_csv('./train.csv',delimiter=',')
print (noisydf.shape)

considered_feat=list(noisydf.columns)

print(considered_feat)
considered_feat.remove('ArrivalDelay')

noisydf=pd.read_csv('fail.csv')
noisy_score= (airline.train_classifier(noisydf))


cleandf=pd.read_csv('pass.csv')
clean_score= (airline.train_classifier(cleandf))

threshold = 40
print ("Clean score is",clean_score)
print ("Noisy score is",noisy_score)

considered_feat.append('ArrivalDelay')

cleanprofile=helper.Dataset(cleandf[considered_feat])
cleanprofilelst=cleanprofile.populate_profiles()

print(cleanprofilelst)


buggyprofiles=helper.Dataset(noisydf[considered_feat])
buggyProfileslst=buggyprofiles.populate_profiles()

benefit_ordering=(get_profile_benefit_ordering(cleanprofilelst,buggyProfileslst,noisydf,cleandf))
#Among the top benefit profiles identify the column


print ((benefit_ordering))
processed=[]


num_interventions=0
for (prof,score) in benefit_ordering:
	if score==0:
		break
	print (prof)
	(col,prof)=identify_column(benefit_ordering,processed)
	print (col,prof,"***************")

	processed.append((prof,col))
	new_df=copy.deepcopy(noisydf)
	new_df[col]=(p.shuffle_transform(new_df[col]))
	try:
		considered_feat.remove('target')
	except:
		a=1
	new_score=airline.train_classifier(new_df)

	num_interventions+=1
	if new_score<threshold:
		print ("FOUND BUG")
		print (prof,col)
		break
	print(col,prof)
	print (col,prof)

print ("number of interventions performed",num_interventions)
