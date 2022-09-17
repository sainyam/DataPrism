import importlib
import json
import os
import pandas as pd
import random
import time
from anchor import anchor_tabular
from helper_latest import Dataset


def transform_column(df,c,p,v):
    try:
        if p == 'min':
            v = float(v)
            df[c].mask(df[c] < v, v, inplace=True)
        elif p == 'max':
            v = float(v)
            df[c].mask(df[c] > v, v, inplace=True)
        elif p == 'length':
            df[c] = df[c].str.slice(0, int(v))
        elif p == 'missing':
            df[c] = df[c].interpolate(method='linear')
    except:
        pass

    if p == 'domain':
        col = list(df[c])
        newcol = []
        for vc in col:
            try:
                vc = vc.replace('(', '')
                vc = vc.replace(')', '')
                newcol.append(vc)
            except:
                newcol.append(vc)
        df[c] = newcol


def transform_corr(df,c,v):
    if v == -0.09499422101046137:
        c_list = df[c].to_list()
        random.shuffle(c_list)
        df[c] = pd.Series(c_list)

def transform_dataset_size(df, v):
    df = (df.iloc[:int(v)])
    return df

def transform_functional(c1, c2, df):
    val_map = {}
    clean_lst = []
    new_df = pd.DataFrame(columns=df.columns)
    for index, row in df.iterrows():
        if row[c1] in val_map.keys():
            if val_map[row[c1]] == row[c2]:
                clean_lst.append(row)
                new_df = new_df.append(row)
                continue
            else:
                row[c2] = val_map[row[c1]]
                new_df = new_df.append(row)
                # val_map[row[c1]]="wrong"
        else:
            clean_lst.append(row)
            new_df = new_df.append(row)
            val_map[row[c1]] = row[c2]

    return new_df

def execute(config_path):
    with open(config_path) as f:
        config = json.load(f)
    my_dir = os.path.dirname(config_path)
    parameters = {}
    labels = []
    module = importlib.import_module(config['python_module'])
    run = getattr(module, config['run'])
    adb = open(os.path.join(my_dir, 'anchors.txt') , 'a')

    for d in config["datasets"]:
        df = pd.read_csv(os.path.join(my_dir, d), encoding=config["encoding"])
        if "columns" in config:
            df = df[config["columns"]]
        dataset = Dataset(df)
        profiles = dataset.populate_profiles()
        for k, v in profiles.items():
            if isinstance(v, str):
                v = 0
            if not v:
                v = 0
            if isinstance(v, list):
                v = 0
            if k[0] == 'length':
                v = v[0]
            if k[0] == 'uniq': continue
            p = k[0] + "|" + k[1]
            if len(k) == 3:
                p += "|" + k[2]
            if p not in parameters:
                parameters[p] = [v]
            else:
                parameters[p].append(v)
        data = os.path.join(my_dir, 'tmp.csv')
        df.to_csv(data, index=False)
        labels.append(str(run(data, config['threshold'], config['bugs'])[0]))
    features = list(parameters.keys())
    train = pd.DataFrame.from_dict(parameters, orient='index').transpose().values
    explainer = anchor_tabular.AnchorTabularExplainer(
        labels,
        features,
        train
    )
    unique = set()
    def workflow_function(sample):
        df_orig = pd.read_csv(os.path.join(my_dir, config['datasets'][1]), encoding=config["encoding"])
        if "columns" in config:
            df_orig = df_orig[config["columns"]]
        predictions = []
        for exp in sample:
            unique.add(str(exp))
            df = df_orig.copy(deep=True)
            for i in range(len(features)):
                k = features[i]
                v = exp[i]
                keys = k.split("|")
                if keys[0] == "dataset_size":
                    df = transform_dataset_size(df, v)
                elif len(keys) == 2:
                    transform_column(df, keys[1], keys[0], v)
                elif keys[0] == "functional" and v == 0.8:
                    df = transform_functional(keys[1], keys[2], df)
                else:
                    transform_corr(df, keys[1], v)

            data = os.path.join(my_dir, 'tmp.csv')
            df.fillna(0).to_csv(data, index=False)
            predictions.append(str(run(data, config['threshold'], config['bugs'])[0]))
            adb.write(str(exp) + '\n')
        adb.write('#\n')
        return pd.Series(predictions)
    start = time.time()
    exp = explainer.explain_instance(train[0], workflow_function, threshold=0.95)
    end = time.time()
    adb.write('Anchor: %s' % (' AND '.join(exp.names())) + '\n')
    adb.write(str(len(unique)) + '\n')
    adb.write(str(end - start))
    adb.close()
