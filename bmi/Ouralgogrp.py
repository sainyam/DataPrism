
import helper,Cardio_pipeline
import pandas as pd
import math
import operator
import copy


def get_distance(clprofile,bugprofile):
	dist=0
	for profile in clprofile.keys():
		dist+=get_profile_distance(clprofile[profile],bugprofile[profile])

	return dist

def get_profile_distance(p1,p2):
	#print (p1,p2)
	if max(p1,p2)==0:
		return 0
	return abs(p1-p2)*1.0/max(p1,p2)
def get_absolute_profile_distance(p1,p2):

	return abs(p1-p2)

def get_profile_benefit_ordering(clprofile,bugprofile):

	benefit={}
	for profile in clprofile.keys():
		if profile[0]=='corr':
			benf=get_absolute_profile_distance(clprofile[profile],bugprofile[profile])
		else:	
			benf=get_profile_distance(clprofile[profile],bugprofile[profile])
		if benf>0:
			benefit[profile]=benf

	sorted_benefit = sorted(benefit.items(), key=operator.itemgetter(1),reverse=True)

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
		if prof in processed:
			continue
		i=1
		while i<len(prof):
			if prof[i] not in column_count.keys():
				column_count[prof[i]]=1
			column_count[prof[i]]+=1
			i+=1

		'''
		found=check_processed_profile(prof[0],processed)
		i=1
		while i<len(prof):
			
			if found:
				if check_col(prof[i],processed):
					i+=1
					continue

			if prof[i] in column_count:
				column_count[prof[i]]+=score
			else:
				column_count[prof[i]]=score
			i+=1
		'''
	sorted_column_score = sorted(column_count.items(), key=operator.itemgetter(1),reverse=True)
	#Get the profile corresponding to this columns
	print (sorted_column_score)
	identified_column_lst=[]#=sorted_column_score[0][0]

	i=0
	while i<len(sorted_column_score):
		curr=sorted_column_score[i]
		if curr[1]==sorted_column_score[0][1]:
			identified_column_lst.append(curr[0])

		i+=1


	prof_count={}
	#Get the profile for this column!
	for (prof,score) in benefit_ordering:
		if prof in processed:
			continue
		i=1
		found=False
		while i<len(prof):
			if prof[i] in identified_column_lst:
				found=True
				break
			i+=1
		if found:
			prof_count[prof]=score
		
	sorted_profile_score = sorted(prof_count.items(), key=operator.itemgetter(1),reverse=True)
	identified_profile=sorted_profile_score[0][0]
	#print(prof_count)
	i=1
	found=False
	while i<len(sorted_profile_score[0][0]):
		if sorted_profile_score[0][0][i] in identified_column_lst:
			found=True
			break
		i+=1
	return (sorted_profile_score[0][0][i],identified_profile,sorted_profile_score[0][0])


p=helper.Profile()
p.add_profile(p.identify_min_profile)

noisydf=pd.read_csv('./test_noisy.csv')

considered_feat=list(noisydf.columns)


noisy_score= (Cardio_pipeline.get_recall(noisydf,considered_feat))

print ("clean now")

cleandf=pd.read_csv('./test_pass.csv')
clean_score= (Cardio_pipeline.get_recall(cleandf,considered_feat))

threshold = 0.6
print ("Clean score is",clean_score)
print ("Noisy score is",noisy_score)

cleanprofile=helper.Dataset(cleandf[considered_feat])
cleanprofilelst=cleanprofile.populate_profiles()

buggyprofiles=helper.Dataset(noisydf[considered_feat])
buggyProfileslst=buggyprofiles.populate_profiles()

benefit_ordering=(get_profile_benefit_ordering(cleanprofilelst,buggyProfileslst))
#Among the top benefit profiles identify the column

processed=[]
num_interventions=0
for (prof,score) in benefit_ordering:
	if score==0:
		break


	(col,prof,fullprofile)=identify_column(benefit_ordering,processed)
	print ("new intervention",prof,col,cleanprofilelst[prof],buggyProfileslst[prof])
	#print (buggyProfileslst[(prof,col)],cleanprofilelst[(prof,col)])


	processed.append(fullprofile)
	new_df=copy.deepcopy(noisydf);
	if prof[0]=='corr':
		new_df[col]=(p.shuffle_transform(new_df[col]))
	elif prof[0]=='min' or prof[0]=='max':
		print ("ratio",cleanprofilelst[prof]*1.0/buggyProfileslst[prof])
		new_df[col]=(p.linear_transform(new_df[col],0,cleanprofilelst[prof]*1.0/buggyProfileslst[prof]))

	new_score=Cardio_pipeline.get_recall(new_df,considered_feat)#Adult.train_classifier(new_df,considered_feat,'sex')
	num_interventions+=1
	if new_score>noisy_score:
		print("some improvement",prof,col,new_score,noisy_score)
		if not prof[0]=='corr':
			print ("ratio",cleanprofilelst[prof],buggyProfileslst[prof])
	if new_score>threshold:
		print ("FOUND BUG",new_score)
		print (prof,col)
		break
	print(col,prof)
	print (col,prof)

print ("number of interventions performed",num_interventions)
