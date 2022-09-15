import argparse
import os
import logging
import json
import shutil
import pandas as pd
from bugdoc.algos.debugging_decision_trees import AutoDebug as Trees
from bugdoc.algos.stacked_shortcut import AutoDebug as StackedShortcut
from bugdoc.utils.quine_mccluskey import prune_tree
from bugdoc.utils.tree import draw_tree
from helper import Dataset
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def main(filename, input_dict,max_iter):
    logging.info("Parameters: " + str(input_dict))
    autodebug = StackedShortcut(separator="#",origin="debug",max_iter=max_iter)
    result = autodebug.run(filename, input_dict, ['result'])
    if len(result) > 1:
        believedecisive, total, _ = result
        logging.info("Shortcut result: "+str(believedecisive))
        if len(believedecisive) > 0:
            max_iter = 0
    autodebug = Trees(separator="#",max_iter=max_iter,k=10,origin="debug")
    believedecisive, t, total = autodebug.run(filename, input_dict, ['result'])
    draw_tree(t)
    results = prune_tree(t, list(input_dict.keys())) if t.results is None else []
    logging.info("Pruning result: " + str(results))
    with open(filename.replace('.vt','.result'),'w+') as f:
        f.write(str(results))


def execute(name, config_path, max_iter):
    with open(config_path) as f:
        config = json.load(f)
    my_dir = os.path.dirname(config_path)
    parameters = {}
    for d in config["datasets"]:
        df = pd.read_csv(os.path.join(my_dir, d), encoding=config["encoding"])
        if "columns" in config:
            df = df[config["columns"]]
        dataset = Dataset(df)
        profiles = dataset.populate_profiles()
        for k, v in profiles.items():
            if k[0] == 'uniq' or k[0] == 'domain': continue
            p = k[0] + "|" + k[1]
            if len(k) == 3:
                p += "|" + k[2]
            if p not in parameters:
                parameters[p] = [v]
            else:
                parameters[p].append(v)

    shutil.copyfile(
        config_path,
        os.path.join(my_dir, 'pipeline_%s_%d.vt' % (name, max_iter))
    )

    main(os.path.join(my_dir, 'pipeline_%s_%d.vt' % (name, max_iter)), parameters, max_iter)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, help="path to config file")
    parser.add_argument("--name", type=str, help="name of the experiment")
    parser.add_argument("--max", type=int, help="max number of interventions")
    args = parser.parse_args()
    name = ""
    if args.name:
        name = args.name
    if args.config:
        if args.max:
            max_iter = args.max
        else:
            max_iter = 100

        execute(name, args.config, max_iter)