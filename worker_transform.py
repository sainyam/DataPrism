import argparse
import ast
import logging
import importlib
import json
import os
import pandas as pd
import random
import sys, traceback
import zmq
from bugdoc.utils.utils import record_python_run
from helper_latest import Dataset

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def transform_column(df, c, p, v):
    try:
        if p == 'min':
            v = float(v)
            df[c].mask(df[c] < v, v, inplace=True)
        elif p == 'max':
            v = float(v)
            df[c].mask(df[c] > v, v, inplace=True)
        elif p == 'length':
            df[c] = df[c].str.slice(0, v)
        elif p == 'missing':
            df[c] = df[c].interpolate(method='linear')
    except:
        pass

    if p == 'domain' and "(" in v:
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


def transform_dataset_size(df, v):
    df = (df.iloc[:v])
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

def transform_corr(df, c, v):
    if v == -0.09499422101046137:
        c_list = df[c].to_list()
        random.shuffle(c_list)
        df[c] = pd.Series(c_list)


def workflow_function(kw_args, config, my_dir):
    df = pd.read_csv(os.path.join(my_dir, config['datasets'][1]), encoding=config["encoding"])
    if "columns" in config:
        df = df[config["columns"]]

    for k, v in kw_args.items():
        keys = k.split("|")
        if keys[0] == "dataset_size":
            df = transform_dataset_size(df, v)
        elif len(keys) == 2:
            transform_column(df, keys[1], keys[0], v)
        elif keys[0] == "functional" and v == 0.5:
            df = transform_functional(keys[1], keys[2], df)
        else:
            transform_corr(df, keys[1], v)

    data = os.path.join(my_dir, 'tmp_transform.csv')
    df.to_csv(data, index=False)
    # print(df)
    module = importlib.import_module(config['python_module'])
    run = getattr(module, config['run'])

    return run(data, config['threshold'], config['bugs'])[0]


parser = argparse.ArgumentParser()
parser.add_argument("--server", type=str, help="host responsible for execution requests")
parser.add_argument("--receive", type=str, help="port to receive messages on")
parser.add_argument("--send", type=str, help="port to send messages to")
args = parser.parse_args()

if args.server:
    host = args.server
else:
    host = 'localhost'

if args.receive:
    receive = args.receive
else:
    receive = '5557'

if args.send:
    send = args.send
else:
    send = '5558'

context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://{0}:{1}".format(host, receive))

# Socket to send messages to
sender = context.socket(zmq.PUSH)
sender.connect("tcp://{0}:{1}".format(host, send))

# Process tasks forever
while True:
    data = receiver.recv_string()
    logging.debug("data: " + data)
    if data == 'kill':
        break
    filename, parameter_list, inputs, outputs, _ = data.split("###")
    parameter_list = ast.literal_eval(parameter_list)
    inputs = ast.literal_eval(inputs)
    outputs = ast.literal_eval(outputs)
    kwargs = {}

    for i in range(len(parameter_list)):
        kwargs[inputs[i]] = parameter_list[i]
    try:
        my_dir = os.path.dirname(filename)
        with open(filename) as f:
            config = json.load(f)
        result = workflow_function(kwargs, config, my_dir)
        logging.debug("result: " + str(result))
        parameter_list.append(str(result))
    except:
        logging.error("Exception in user code:")
        logging.error("-" * 60)
        traceback.print_exc(file=sys.stdout)
        logging.error("-" * 60)
        parameter_list.append(str(False))

    kwargs['result'] = parameter_list[-1]
    record_python_run(kwargs, filename.replace('json', 'vt'))
    sender.send_string(str(parameter_list))
