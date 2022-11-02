
import helper,test_proxy
import numpy as np
import pandas as pd
import math
import operator
import copy
import prose.datainsights as di


def get_distance(clprofile,bugprofile):
	dist=0
	for profile in clprofile.keys():
		dist+=get_profile_distance(clprofile[profile],bugprofile[profile])

	return dist

def get_profile_distance(p1,p2):
	
	if max(abs(p1),abs(p2))==0:
		return 0
	return abs(p1-p2)*1.0/max(abs(p1),abs(p2))
def get_absolute_profile_distance(p1,p2):

	return abs(p1-p2)
def get_domain_distance(l1,l2):
	inter=list(set(l1)&set(l2))
	l3=[]
	l3.extend(l1)
	l3.extend(l2)
	l3=list(set(l3))
	return  1-len(inter)*1.0/len(l3)

def clean_dataset_size(prof,new_df,th):
	new_size=int(new_df.shape[0]*th)
	print ("size is ",new_size,th)
	new_df= (new_df.iloc[:new_size])
	return new_df
def clean_regexp(prof,df):
	col=list(df[prof[1]])

	newcol=[]
	for v in col:
		try:
			v=v.replace('(','')
			v=v.replace(')','')
			newcol.append(v)
		except:
			newcol.append(v)

	df[prof[1]]=newcol
	print (df['Phone'])
	return df

def clean_functional(c1,c2,df):
    val_map={}
    clean_lst=[]
    new_df=pd.DataFrame(columns=df.columns)
    for index,row in df.iterrows():
        if row[c1] in val_map.keys():
            if val_map[row[c1]]==row[c2]:
                clean_lst.append(row)
                new_df=new_df.append(row)
                continue
            else:
            	row[c2]=val_map[row[c1]]
            	new_df=new_df.append(row)
                #val_map[row[c1]]="wrong"
        else:
            clean_lst.append(row)
            new_df=new_df.append(row)
            val_map[row[c1]]=row[c2]
            

    #new_df=pd.DataFrame(clean_lst,columns=df.columns) 
    return new_df

#########################
###Benefit calculation###
#########################
def get_profile_benefit_ordering(clprofile,bugprofile,bugdf,cleandf):


	#####If a column in numerical in one table and textual in another then we need to just identify the number of textual rows and remove those


	print (clprofile)
	benefit={}

	#Add a distance for all profiles here 
	for profile in clprofile.keys():
		try:
			if profile[0]=='conformance':
				benf=0#clprofile[profile].evaluate(bugdf).avg_violation
				
			elif profile[0]=='corr' or profile[0]=='functional' or profile[0]=='missing' or profile[0]=='outlier' or profile[0]=='uniq':
				viol=get_absolute_profile_distance(clprofile[profile],bugprofile[profile])
				if profile[0]=='functional' or profile[0]=='missing' or profile[0]=='outlier' or profile[0]=='uniq':
					benf=viol*bugprofile[profile]
				else:
					benf=viol


				print(benf,clprofile[profile],bugprofile[profile],profile)
			elif profile[0]=='domain':
				benf=get_domain_distance(clprofile[profile],bugprofile[profile])
			elif profile[0]=='length':
				benf=get_absolute_profile_distance(clprofile[profile][-1],bugprofile[profile][-1])
			else:
				print (profile)
				benf=get_profile_distance(clprofile[profile],bugprofile[profile])
				
				#print(benf,clprofile[profile],bugprofile[profile],profile)
		except:
			benf=0
		if benf>0:
			benefit[profile]=benf

	sorted_benefit = sorted(benefit.items(), key=operator.itemgetter(1),reverse=True)
	print(sorted_benefit,len(sorted_benefit))

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
			else:
				column_count[prof[i]]=1
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
	print (len(sorted_column_score))
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

	#print ("sorted profile score",sorted_profile_score)
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


noisydf=pd.read_csv('../datasets/amazon/dirty.csv')

considered_feat=list(noisydf.columns)


noisy_score= (test_proxy.get_runtime(noisydf[considered_feat]))

print ("clean now")

cleandf=pd.read_csv('../datasets/amazon/clean.csv')
clean_score= (test_proxy.get_runtime(cleandf[considered_feat]))

threshold = 0.002
print ("Clean score is",clean_score)
print ("Noisy score is",noisy_score)

cleanprofile=helper.Dataset(cleandf[considered_feat])
cleanprofilelst=cleanprofile.populate_profiles()
print ("clean",cleanprofilelst)

buggyprofiles=helper.Dataset(noisydf[considered_feat])
buggyProfileslst=buggyprofiles.populate_profiles()

print (buggyProfileslst)


maxval=1
for prof in cleanprofilelst.keys():
	if prof[0]=='corr':
		if cleanprofilelst[prof]>maxval:
			maxval=cleanprofilelst[prof]

for prof in buggyProfileslst.keys():
	if prof[0]=='corr':
		if buggyProfileslst[prof]>maxval:
			maxval=buggyProfileslst[prof]


print (maxval)

for prof in cleanprofilelst.keys():
	if prof[0]=='corr':
		cleanprofilelst[prof]/=maxval

for prof in buggyProfileslst.keys():
	if prof[0]=='corr':
		buggyProfileslst[prof]/=maxval


def remove_characters(new_df):

    lst=[]
    for iter,row in new_df.iterrows():
        try:
            lst.append(row['text'][:100])
        except:
            lst.append('')
            continue
    new_df['text']=lst
    print(new_df)
    return new_df
import time
start=time.time()

benefit_ordering=(get_profile_benefit_ordering(cleanprofilelst,buggyProfileslst,noisydf,cleandf))

#Among the top benefit profiles identify the column


print (benefit_ordering)

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
		new_df[col]=new_df[col]
		#print ("ratio",cleanprofilelst[prof]*1.0/buggyProfileslst[prof])
		#new_df[col]=(p.linear_transform(new_df[col],0,cleanprofilelst[prof]*1.0/buggyProfileslst[prof]))
	if prof[0]=='functional' and cleanprofilelst[prof]>0.99:# and prof[1]=='ZipCode': and prof[2]=='City':
		new_df=clean_functional(prof[1],prof[2],new_df)
		print ("identified")
		#print (new_df)
	if prof[0]=='domain':# and prof[1]=='Phone':
		new_df=clean_regexp(prof,new_df)
	if prof[0]=='dataset_size':
		print (cleandf.shape,noisydf.shape,new_df.shape)
		thres=cleandf.shape[0]*1.0/noisydf.shape[0]
		new_df=clean_dataset_size(prof,new_df,thres)
	if prof[0]=='length':
		new_df=remove_characters(new_df)
	new_score=test_proxy.get_runtime(new_df[considered_feat])#Adult.train_classifier(new_df,considered_feat,'sex')

	print (new_score)
	num_interventions+=1
	if new_score>noisy_score:
		print("some improvement",prof,col,new_score,noisy_score)
		new_df.index = np.arange(0, len(new_df))

		noisydf=new_df
		noisy_score=new_score
		#buggyprofiles=helper.Dataset(noisydf[considered_feat])
		#buggyProfileslst=buggyprofiles.populate_profiles()
		#for prof in buggyProfileslst.keys():
		#	if prof[0]=='corr':
		#		buggyProfileslst[prof]/=maxval
		#benefit_ordering=(get_profile_benefit_ordering(cleanprofilelst,buggyProfileslst,noisydf,cleandf))




	if new_score==1:
		print ("FOUND BUG",new_score)
		print (prof,col)
		print (new_df)
		break
	print(col,prof)
	print (col,prof)

end=time.time()
fout=open("nog.txt","w")
fout.write(str(num_interventions)+" "+str(end-start))
fout.close()
print ("number of interventions performed",num_interventions)
