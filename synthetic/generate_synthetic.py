import json
import os
import numpy as np
import pandas as pd
import random
import shutil


def generate_bugs(num_attr, len_bug, num_bugs):
    bugs = []

    for _ in range(num_bugs):
        bugs.append(list(np.random.choice(range(num_attr), len_bug, replace=False)))

    return bugs


def generate_datasets(num_attrs, overlapped, pipeline_module):
    df_pass = pd.DataFrame()
    df_fail = pd.DataFrame()

    j = 0
    while j < num_attrs:
        lst_pass = []
        lst_fail = []
        i = 0
        while i < 1000:
            lst_pass.append(random.randint(0, 10))
            if j not in overlapped:
                if 'missing' in pipeline_module:
                    lst_fail.append(random.choices([random.randint(0, 10), None], weights=[0.1,0.9])[0])
                else:
                    lst_fail.append(random.randint(9, 100))
            else:
                lst_fail.append(random.randint(0, 10))
            i += 1
        df_pass[j] = lst_pass
        df_fail[j] = lst_fail
        j += 1
    return df_pass, df_fail


def generate(max_attrs, output_folder, pipeline_module, threshold):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    experiments_list_path = output_folder + '/list.txt'
    experiments_list_file = open(experiments_list_path, "a")
    for num_attrs in range(15, 16):

        for len_bugs in range(2, 3):

            for len_dis in range(2,12):

                bugs = generate_bugs(num_attrs,len_bugs,len_dis)
                bug_cols = {x for l in bugs for x in l} # Find columns in bugs

                #for overlap in range(1, num_attrs - len(bug_cols)):
                print(num_attrs,len(bug_cols))
                overlap = 2 #np.random.choice(range(max(1,num_attrs - len(bug_cols))))
                overlapped = np.random.choice([c for c in range(num_attrs) if c not in bug_cols ], overlap, replace=False)
                df_pass, df_fail = generate_datasets(num_attrs, overlapped, pipeline_module)
                pipeline_name = os.path.join(output_folder,"synthetic_%d_%d_%d_%d" % (
                    num_attrs,
                    overlap,
                    len(bugs),
                    max([len(bug) for bug in bugs])
                ))
                os.makedirs(pipeline_name)

                df_pass.to_csv(os.path.join(pipeline_name,"pass.csv"))
                df_fail.to_csv(os.path.join(pipeline_name, "fail.csv"))

                config = {
                    "python_module": pipeline_module,
                    "run": "run",
                    "datasets":
                        [
                            "pass.csv",
                            "fail.csv"
                        ],
                    "columns": [str(a) for a in range(num_attrs)],
                    "encoding": None,
                    "threshold": threshold,
                    "bugs": [[str(c) for c in bug] for bug in bugs]
                }
                with open(os.path.join(pipeline_name,"config.json"), 'w') as outfile:
                    json.dump(config,outfile)
                experiments_list_file.write(pipeline_name + '\n')
    experiments_list_file.close()

if __name__ == "__main__":
    generate(15, "./SIGMOD_disjunctions_2/", "synthetic.pipeline", "2")
    generate(15, "./SIGMOD_disjunctions_4/", "synthetic.pipeline", "4")
    generate(15, "./SIGMOD_disjunctions_8/", "synthetic.pipeline", "8")
    generate(15, "./SIGMOD_disjunctions_16/", "synthetic.pipeline", "16")
    generate(15, "./SIGMOD_disjunctions_32/", "synthetic.pipeline", "32")

    generate(15, "./SIGMOD_disjunctions_missing_2/", "synthetic.pipeline_missing", "2")
    generate(15, "./SIGMOD_disjunctions_missing_4/", "synthetic.pipeline_missing", "4")
    generate(15, "./SIGMOD_disjunctions_missing_8/", "synthetic.pipeline_missing", "8")
    generate(15, "./SIGMOD_disjunctions_missing_16/", "synthetic.pipeline_missing", "16")
    generate(15, "./SIGMOD_disjunctions_missing_32/", "synthetic.pipeline_missing", "32")
