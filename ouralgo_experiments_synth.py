import copy
from helper_synth import Profile, Dataset
import importlib
import json
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

def get_distance(clprofile, bugprofile):
    dist = 0
    for profile in clprofile.keys():
        dist += get_profile_distance(clprofile[profile], bugprofile[profile])

    return dist


def get_profile_distance(p1, p2):
    if type(p1) is tuple:
        return abs(p1[0] - p2[0])
    else:
        return abs(p1 - p2)


def get_profile_benefit_ordering(clprofile, bugprofile):
    benefit = {}
    for profile in clprofile.keys():
        benefit[profile] = get_profile_distance(clprofile[profile], bugprofile[profile])

    sorted_benefit = sorted(benefit.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_benefit


def check_processed_profile(prof, processed):
    for (p, col) in processed:
        if p == prof:
            return True
    return False


def check_col(col, processed):
    for (p, column) in processed:
        if col == column:
            return True
    return False


# Processed is a list of tuples where first element is profile name and 2nd element is column name
def identify_column(benefit_ordering, processed):
    column_count = {}
    for (prof, score) in benefit_ordering:

        found = check_processed_profile(prof[0], processed)
        i = 1
        while i < len(prof):

            if found:
                if check_col(prof[i], processed):
                    i += 1
                    continue

            if prof[i] in column_count:
                column_count[prof[i]] += score
            else:
                column_count[prof[i]] = score
            i += 1
    print(column_count)
    sorted_column_score = sorted(column_count.items(), key=operator.itemgetter(1), reverse=True)
    # Get the profile corresponding to this columns
    print (sorted_column_score)
    identified_column = sorted_column_score[0][0]

    prof_count = {}
    # Get the profile for this column!
    for (prof, score) in benefit_ordering:

        found = check_processed_profile(prof[0], processed)
        i = 1
        while i < len(prof):

            if found:
                if check_col(prof[i], processed):
                    i += 1
                    continue
            # print (prof,score,identified_column)
            if prof[i] == identified_column:
                if prof[0] in prof_count.keys():
                    prof_count[prof[0]] += score
                else:
                    prof_count[prof[0]] = score

            i += 1
    sorted_profile_score = sorted(prof_count.items(), key=operator.itemgetter(1), reverse=True)
    identified_profile = sorted_profile_score[0][0]
    # print(prof_count)
    return (identified_column, identified_profile)

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
    cleanprofilelst = {k:v for k,v in cleanprofile.populate_profiles().items() if k[0] not in "corr|functional"}

    buggyprofiles = Dataset(noisydf)
    buggyProfileslst = {k:v for k,v in buggyprofiles.populate_profiles().items() if k[0] not in "corr|functional"}

    print('buggyProfileslst',buggyProfileslst)
    print('cleanprofilelst', cleanprofilelst)

    benefit_ordering = (get_profile_benefit_ordering(cleanprofilelst, buggyProfileslst))
    # Among the top benefit profiles identify the column
    processed = []
    num_interventions = 0
    try:
        for (prof, score) in benefit_ordering:
            if score == 0:
                break
            print(prof)
            (col, prof) = identify_column(benefit_ordering, processed)
            processed.append((prof, col))
            new_df = copy.deepcopy(noisydf)

            if not(prof == 'corr'):
                print(cleanprofilelst[(prof,col)], prof, col)
                transform_column(new_df, col, prof, cleanprofilelst[(prof,col)])
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
                    adb.write(str((prof, col, cleanprofilelst[(prof, col)])) + '\n')
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