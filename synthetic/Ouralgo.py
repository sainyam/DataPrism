
import helper,pipeline
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
	return abs(p1-p2)

def get_profile_benefit_ordering(clprofile,bugprofile):
	benefit={}
	for profile in clprofile.keys():
		benefit[profile]=get_profile_distance(clprofile[profile],bugprofile[profile])

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
#Processed is a list oftuples where first element is profile name and 2nd element is column nam
def identify_column(benefit_ordering,processed):
	column_count={}
	for (prof,score) in benefit_ordering:

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
	sorted_column_score = sorted(column_count.items(), key=operator.itemgetter(1),reverse=True)
	#Get the profile corresponding to this columns
	#print (sorted_column_score)

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
	#print(prof_count)
	return (identified_column,identified_profile)


p=helper.Profile()
p.add_profile(p.identify_min_profile)

noisydf=pd.read_csv('./fail100.csv')

considered_feat=list(noisydf.columns)

noisy_score= pipeline.run_pipeline(noisydf)



cleandf=pd.read_csv('./pass.csv')
clean_score= pipeline.run_pipeline(cleandf)

threshold = 2
print ("Clean score is",clean_score)
print ("Noisy score is",noisy_score)

cleanprofile=helper.Dataset(cleandf[considered_feat])
cleanprofilelst=cleanprofile.populate_profiles()

buggyprofiles=helper.Dataset(noisydf[considered_feat])
buggyProfileslst=buggyprofiles.populate_profiles()


print (cleanprofilelst)

print ("-----------------------------")
print(buggyProfileslst)

benefit_ordering=(get_profile_benefit_ordering(cleanprofilelst,buggyProfileslst))
#Among the top benefit profiles identify the column


print(benefit_ordering)

processed=[]
num_interventions=0

for (profile,score) in benefit_ordering:
	if score==0 or len(processed)==len(benefit_ordering):
		break

	#print (prof)
	col=profile[1]
	prof=profile[0]
	#(col,prof)=identify_column(benefit_ordering,processed)

	print ("current profile",col,prof)

	processed.append((prof,col))
	new_df=copy.deepcopy(noisydf)

	rangeval=[buggyProfileslst[profile],cleanprofilelst[profile]]
	#print (rangeval)
	new_df[col]=(p.apply_transformation(new_df[col],col,prof,rangeval,buggyProfileslst,cleanprofilelst))

	new_score=pipeline.run_pipeline(new_df)
	num_interventions+=1
	#print (new_score,rangeval,new_df)
	if new_score<threshold:
		print ("FOUND BUG")
		print (prof,col)
		break
	
print ("number of interventions performed",num_interventions)
print (" number of differing profiles",len(benefit_ordering))
