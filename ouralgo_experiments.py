import copy
from helper_latest import Profile, Dataset
import importlib
import json
import math
import operator
import os
import pandas as pd
import random
import time




def transform_column(df,c,p,v):
    if p == 'min':
        df[c].mask(df[c] < v, v, inplace=True)
    elif p == 'max':
        df[c].mask(df[c] > v, v, inplace=True)
    elif p == 'length':
        df[c] = df[c].str.slice(0,v[0])
    elif p == 'missing':
        df[c] = df[c].interpolate(method='linear')


def transform_corr(df,c):
        c_list = df[c].to_list()
        random.shuffle(c_list)
        df[c] = pd.Series(c_list)

def get_distance(clprofile,bugprofile):
    dist=0
    for profile in clprofile.keys():
        dist+=get_profile_distance(clprofile[profile],bugprofile[profile])

    return dist

def get_profile_distance(p1,p2):
    #print (p1,p2)
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



#########################
###Benefit calculation###
#########################
def get_profile_benefit_ordering(clprofile,bugprofile,bugdf,cleandf):
    print (clprofile)
    benefit={}

    #Add a distance for all profiles here 
    for profile in clprofile.keys():
        if profile[0]=='conformance':
            print(bugdf.shape)
            benf=clprofile[profile].evaluate(bugdf).avg_violation
            
        elif profile[0]=='corr' or profile[0]=='functional' or profile[0]=='missing' or profile[0]=='outlier' or profile[0]=='uniq':
            viol=get_absolute_profile_distance(clprofile[profile],bugprofile[profile])
            if profile[0]=='functional' or profile[0]=='missing' or profile[0]=='outlier' or profile[0]=='uniq':
                benf=viol*bugprofile[profile]
            else:
                benf=viol


            print(benf,clprofile[profile],bugprofile[profile],profile)
        elif profile[0]=='length':
                benf=get_absolute_profile_distance(clprofile[profile][-1],bugprofile[profile][-1])
        elif profile[0]=='domain':
            benf=get_domain_distance(clprofile[profile],bugprofile[profile])
        else:
            print (profile)
            benf=get_profile_distance(clprofile[profile],bugprofile[profile])
            print(benf,clprofile[profile],bugprofile[profile],profile)
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

    print ("sorted profile score",sorted_profile_score)
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

examples = []


experiments = open("./SIGMOD_conjunctions_2/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_conjunctions_4/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_conjunctions_8/list.txt",'r')
examples += experiments.readlines()
experiments.close()


experiments = open("./SIGMOD_conjunctions_16/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_conjunctions_32/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_conjunctions_missing_2/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_conjunctions_missing_4/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_conjunctions_missing_8/list.txt",'r')
examples += experiments.readlines()
experiments.close()


experiments = open("./SIGMOD_conjunctions_missing_16/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_conjunctions_missing_32/list.txt",'r')
examples += experiments.readlines()
experiments.close()


experiments = open("./SIGMOD_disjunctions_2/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_disjunctions_4/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_disjunctions_8/list.txt",'r')
examples += experiments.readlines()
experiments.close()


experiments = open("./SIGMOD_disjunctions_16/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_disjunctions_32/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_disjunctions_missing_2/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_disjunctions_missing_4/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_disjunctions_missing_8/list.txt",'r')
examples += experiments.readlines()
experiments.close()


experiments = open("./SIGMOD_disjunctions_missing_16/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_disjunctions_missing_32/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_single_2/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_single_4/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_single_8/list.txt",'r')
examples += experiments.readlines()
experiments.close()


experiments = open("./SIGMOD_single_16/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_single_32/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_single_missing_2/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_single_missing_4/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_single_missing_8/list.txt",'r')
examples += experiments.readlines()
experiments.close()


experiments = open("./SIGMOD_single_missing_16/list.txt",'r')
examples += experiments.readlines()
experiments.close()

experiments = open("./SIGMOD_single_missing_32/list.txt",'r')
examples += experiments.readlines()
experiments.close()


for e in examples:
    print('example',e)
    adb = open(os.path.join(e.strip(), "dp.txt"), "a")
    p = Profile()
    p.add_profile(p.identify_min_profile)

    noisy_score = None
    noisydf = None
    clean_score = None
    cleandf = None

    with open(os.path.join(e.strip(), "config.json")) as f:
        config = json.load(f)
    for d in config["datasets"]:
        df = pd.read_csv(os.path.join(e.strip(), d), encoding=config["encoding"])
        if "columns" in config:
            df = df[config["columns"]]
        data = os.path.join(e.strip(), 'tmp_ouralgo.csv')
        df.to_csv(data, index=False)
        module = importlib.import_module(config['python_module'])
        run = getattr(module, config['run'])
        is_clean, new_score = run(data, config['threshold'], config['bugs'])
        if is_clean:
            clean_score = new_score
            cleandf = df
        else:
            noisy_score = new_score
            noisydf = df
    start = time.time()
    print ("Clean score is", clean_score)
    print ("Noisy score is", noisy_score)

    cleanprofile = Dataset(cleandf)
    cleanprofilelst = {k:v for k,v in cleanprofile.populate_profiles().items() if k[0] not in "corr|functional|conformance"}

    buggyprofiles = Dataset(noisydf)
    buggyProfileslst = {k:v for k,v in buggyprofiles.populate_profiles().items() if k[0] not in "corr|functional|conformance"} 


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


    print('buggyProfileslst',buggyProfileslst)
    print('cleanprofilelst', cleanprofilelst)

    benefit_ordering = (get_profile_benefit_ordering(cleanprofilelst,buggyProfileslst,noisydf,cleandf))
    # Among the top benefit profiles identify the column
    processed = []
    num_interventions = 0
    try:
        for (prof, score) in benefit_ordering:
            if score == 0:
                break
            print(prof)
            (col,prof,fullprofile)=identify_column(benefit_ordering,processed)
            print ("new intervention",prof,col,cleanprofilelst[prof],buggyProfileslst[prof])
            processed.append(fullprofile)
            new_df = copy.deepcopy(noisydf)

            if not(prof == 'corr'):
                print(cleanprofilelst[prof], prof, col)
                transform_column(new_df, col, prof, cleanprofilelst[prof])
            else:
                transform_corr(new_df, col)

            #new_df[col] = (p.shuffle_transform(new_df[col]))

            # Saving transformed data
            new_df.to_csv(data, index=False)
            _, new_score = run(data, config['threshold'], config['bugs'])
            num_interventions += 1
            if new_score < noisy_score:
                print ("FOUND BUG")
                print (prof, col)
                if not (prof == 'corr'):
                    adb.write(str((prof, col, cleanprofilelst[prof])) + '\n')
                else:
                    adb.write(str((prof, col)) + '\n')

                break
            print(col, prof)
            print (col, prof)
    except:
        pass
    end = time.time()
    adb.write(str(end - start) + '\n')
    adb.write(str(num_interventions) + '\n')
    print ("number of interventions performed", num_interventions)
    adb.close()
