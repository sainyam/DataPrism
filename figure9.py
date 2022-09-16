import matplotlib.pyplot as plt
import matplotlib
import  numpy as np
from matplotlib.ticker import MaxNLocator
from matplotlib.font_manager import FontProperties

from matplotlib import rc
from matplotlib import rcParams
rcParams['font.family'] = 'serif'
rc('text', usetex=False)

import json
import os
import pandas as pd
import numpy as np
from helper_latest import Dataset

diverging_horizontal_dict = {'domain':{}, 'missing':{}}
attributes_horizontal_dict =  {'domain':{}, 'missing':{}}
exposer_attr_dict =  {'domain':{}, 'missing':{}}
bugdoc_attr_dict =  {'domain':{}, 'missing':{}}
anchor_attr_dict =  {'domain':{}, 'missing':{}}
gt_attr_dict =  {'domain':{}, 'missing':{}}
exposer_diverging_dict =  {'domain':{}, 'missing':{}} 
bugdoc_diverging_dict =  {'domain':{}, 'missing':{}}
anchor_diverging_dict =  {'domain':{}, 'missing':{}}
gt_diverging_dict =  {'domain':{}, 'missing':{}}
horizontal_dict =  {}
exposer_dict =  {}
bugdoc_dict =  {}
anchor_dict =  {}
gt_dict =  {}
horizontal_dict['conjunctions'] =  {'domain':{}, 'missing':{}}
exposer_dict['conjunctions'] =  {'domain':{}, 'missing':{}}
bugdoc_dict['conjunctions'] =  {'domain':{}, 'missing':{}}
anchor_dict['conjunctions'] =  {'domain':{}, 'missing':{}}
gt_dict['conjunctions'] =  {'domain':{}, 'missing':{}}
horizontal_dict['disjunctions'] =  {'domain':{}, 'missing':{}}
exposer_dict['disjunctions'] =  {'domain':{}, 'missing':{}}
bugdoc_dict['disjunctions'] =  {'domain':{}, 'missing':{}}
anchor_dict['disjunctions'] =  {'domain':{}, 'missing':{}}
gt_dict['disjunctions'] =  {'domain':{}, 'missing':{}}



diverging_horizontal_time = [69, 1853, 6157, 12804, 22199, 33746, 48216, 65069, 84225, 106082, 130432, 157071, 186566, 217744, 252107, 288754, 329347, 370388]
attributes_horizontal_time = [10, 60, 110, 160, 210, 260, 310, 360, 410, 460, 510, 560, 610, 660, 710, 760, 810, 860]

exposer_attr_time = [0.029430866241455078, 0.7266449928283691, 3.234330177307129, 4.886771202087402, 13.783616065979004, 9.70192003250122, 28.15203595161438, 24.933053016662598, 104.19999694824219, 38.69125509262085, 30.80706810951233, 236.8483488559723, 425.32921290397644, 52.220191955566406, 497.4534101486206, 694.9491801261902, 15332.690306186676, 19598.287848234177]
gt_attr_time = [0.16323471069335938, 0.9372751712799072, 2.322911024093628, 5.261242866516113, 7.595234632492065, 12.380239009857178, 18.48108410835266, 24.965620040893555, 31.865647077560425, 53.49918603897095, 66.77600812911987, 80.55005288124084, 87.90629506111145, 104.62124395370483, 103.66580986976624, 138.5898938179016, 117.04100513458252, 184.0877969264984]
exposer_diverging_time = [0.029430866241455078, 0.7266449928283691, 3.234330177307129, 4.886771202087402, 13.783616065979004, 9.70192003250122, 28.15203595161438, 24.933053016662598, 104.19999694824219, 38.69125509262085, 30.80706810951233, 236.8483488559723, 425.32921290397644, 52.220191955566406, 497.4534101486206, 694.9491801261902, 15332.690306186676, 19598.287848234177]
gt_diverging_time = [0.16323471069335938, 0.9372751712799072, 2.322911024093628, 5.261242866516113, 7.595234632492065, 12.380239009857178, 18.48108410835266, 24.965620040893555, 31.865647077560425, 53.49918603897095, 66.77600812911987, 80.55005288124084, 87.90629506111145, 104.62124395370483, 103.66580986976624, 138.5898938179016, 117.04100513458252, 184.0877969264984]


pvts = [ "domain", "missing"]
causes = ['single','conjunctions', 'disjunctions']
for pvt in pvts:
    for t in [2,4,8,16, 32]:
        for c in causes:
            if 'single' in c:
                diverging_counts = {}
                attribute_counts = {}
                experiments = open("./SIGMOD_single%s_%d/list.txt" % ("" if "domain" in pvt else "_missing", t), 'r')
                examples = experiments.readlines()
                experiments.close()
                for e in examples:
                    my_dir = e.strip()
                    # _,_,_, dis, con = my_dir.split('_')
                    #
                    # if int(dis) > 1 or int(con) > 1: continue
    
                    with open(os.path.join(my_dir, "config.json")) as f:
                        config = json.load(f)
                    my_dict = {}
                    for d in config["datasets"]:
                        df = pd.read_csv(os.path.join(my_dir, d), encoding=config["encoding"])
                        if "columns" in config:
                            df = df[config["columns"]]
                        dataset = Dataset(df)
                        profiles = dataset.populate_profiles()
                        for k, v in profiles.items():
                            if k not in my_dict:
                                my_dict[k] = [v]
                            elif v not in my_dict[k]:
                                my_dict[k].append(v)

                    diverging = [k for k in my_dict if len(my_dict[k]) > 1]
                    num_diverging = len(diverging)
                    num_attributes = int(e.split('_')[4 if "missing" in pvt else 3])

                    if os.path.exists(os.path.join(e.strip(), "pipeline_transform_200.adb")):
                        f = open(os.path.join(e.strip(), "pipeline_transform_200.adb"), 'r')
                        experiment_lines = f.readlines()
                        f.close()
                        bugdoc_inter = len(experiment_lines)
                    else:
                        bugdoc_inter = 0

                    if os.path.exists(os.path.join(e.strip(), "dp.txt")):
                        f = open(os.path.join(e.strip(), "dp.txt"), 'r')
                        experiment_lines = f.readlines()
                        f.close()
                        dataexposer_inter = int(experiment_lines[-1].strip())
                    else:
                        dataexposer_inter = 0
                    
                    if os.path.exists(os.path.join(e.strip(), "grptest.txt")):
                        f = open(os.path.join(e.strip(), "grptest.txt"), 'r')
                        experiment_lines = f.readlines()
                        f.close()
                        grptest_inter = int(experiment_lines[-1].strip())
                    else:
                        grptest_inter = 0
                    if os.path.exists(os.path.join(e.strip(), "anchor.txt")):
                        f = open(os.path.join(e.strip(), "anchor.txt"), 'r')
                        experiment_lines = f.readlines()
                        f.close()
                    else:
                        experiment_lines = []

                    anchor_inter = 0
                    for line in experiment_lines:
                        if "[" in line:
                            anchor_inter += 1

                    if num_attributes not in attribute_counts:
                        attribute_counts[num_attributes] = {
                            "dataexposer": [dataexposer_inter],
                            "bugdoc": [bugdoc_inter],
                            "anchor": [anchor_inter],
                            "grptest": [grptest_inter]
                        }       
                    else:
                        attribute_counts[num_attributes]["dataexposer"].append(dataexposer_inter)
                        attribute_counts[num_attributes]["bugdoc"].append(bugdoc_inter)
                        attribute_counts[num_attributes]["anchor"].append(anchor_inter)
                        attribute_counts[num_attributes]["grptest"].append(grptest_inter)


                    if num_diverging not in diverging_counts:
                        diverging_counts[num_diverging] = {
                            "dataexposer": [dataexposer_inter],
                            "bugdoc": [bugdoc_inter],
                            "anchor": [anchor_inter],
                            "grptest": [grptest_inter]
                        }       
                    else:
                        diverging_counts[num_diverging]["dataexposer"].append(dataexposer_inter)
                        diverging_counts[num_diverging]["bugdoc"].append(bugdoc_inter)
                        diverging_counts[num_diverging]["anchor"].append(anchor_inter)
                        diverging_counts[num_diverging]["grptest"].append(grptest_inter)

                diverging_horizontal = sorted(list(diverging_counts.keys()))
                attributes_horizontal = sorted(list(attribute_counts.keys()))
                diverging_horizontal_dict[pvt][t] = diverging_horizontal
                attributes_horizontal_dict[pvt][t] = attributes_horizontal

                exposer_attr = [np.mean(attribute_counts[count]['dataexposer']) for count in attributes_horizontal]
                bugdoc_attr = [np.mean(attribute_counts[count]['bugdoc']) for count in attributes_horizontal]
                anchor_attr = [np.mean(attribute_counts[count]['anchor']) for count in attributes_horizontal]
                grptest_attr = [np.mean(attribute_counts[count]['grptest']) for count in attributes_horizontal]
                exposer_attr_dict[pvt][t] = exposer_attr
                bugdoc_attr_dict[pvt][t] = bugdoc_attr
                anchor_attr_dict[pvt][t] = anchor_attr
                gt_attr_dict[pvt][t] = grptest_attr

                exposer_diverging = [np.mean(diverging_counts[count]['dataexposer']) for count in diverging_horizontal]
                bugdoc_diverging = [np.mean(diverging_counts[count]['bugdoc']) for count in diverging_horizontal]
                anchor_diverging = [np.mean(diverging_counts[count]['anchor']) for count in diverging_horizontal]
                grptest_diverging = [np.mean(diverging_counts[count]['grptest']) for count in diverging_horizontal]
                exposer_diverging_dict[pvt][t] = exposer_diverging
                bugdoc_diverging_dict[pvt][t] = bugdoc_diverging
                anchor_diverging_dict[pvt][t] = anchor_diverging
                gt_diverging_dict[pvt][t] = grptest_diverging
            elif 'time' in c:
                diverging_counts = {}
                attribute_counts = {}
                experiments = open("./SIGMOD_time/list.txt", 'r')
                examples = experiments.readlines()
                experiments.close()
                for e in examples:
                    my_dir = e.strip()

                    with open(os.path.join(my_dir, "config.json")) as f:
                        config = json.load(f)
                    my_dict = {}
                    for d in config["datasets"]:
                        df = pd.read_csv(os.path.join(my_dir, d), encoding=config["encoding"])
                        if "columns" in config:
                            df = df[config["columns"]]
                        dataset = Dataset(df)
                        profiles = dataset.populate_profiles()
                        for k, v in profiles.items():
                            if k not in my_dict:
                                my_dict[k] = [v]
                            elif v not in my_dict[k]:
                                my_dict[k].append(v)

                    diverging = [k for k in my_dict if len(my_dict[k]) > 1]
                    num_diverging = len(diverging)
                    num_attributes = int(e.split('_')[2])

                    # f = open(os.path.join(e.strip(), "pipeline_transform_201.adb"), 'r')
                    # experiment_lines = f.readlines()
                    # f.close()

                    # bugdoc_inter = len(experiment_lines)

                    f = open(os.path.join(e.strip(), "dp.txt"), 'r')
                    experiment_lines = f.readlines()
                    f.close()
                    dataexposer_inter = float(experiment_lines[-2].strip())

                    f = open(os.path.join(e.strip(), "grptest.txt"), 'r')
                    experiment_lines = f.readlines()
                    f.close()
                    grptest_inter = float(experiment_lines[-2].strip())

                    # f = open(os.path.join(e.strip(), "anchor.txt"), 'r')
                    # experiment_lines = f.readlines()
                    # f.close()
                    # anchor_inter = 0
                    # for line in experiment_lines:
                    #     if "[" in line:
                    #         anchor_inter += 1

                    if num_attributes not in attribute_counts:
                        attribute_counts[num_attributes] = {
                            "dataexposer": [dataexposer_inter],
                            # "bugdoc": [bugdoc_inter],
                            # "anchor": [anchor_inter],
                            "grptest": [grptest_inter]
                        }
                    else:
                        attribute_counts[num_attributes]["dataexposer"].append(dataexposer_inter)
                        # attribute_counts[num_attributes]["bugdoc"].append(bugdoc_inter)
                        # attribute_counts[num_attributes]["anchor"].append(anchor_inter)
                        attribute_counts[num_attributes]["grptest"].append(grptest_inter)

                    if num_diverging not in diverging_counts:
                        diverging_counts[num_diverging] = {
                            "dataexposer": [dataexposer_inter],
                            # "bugdoc": [bugdoc_inter],
                            # "anchor": [anchor_inter],
                            "grptest": [grptest_inter]
                        }
                    else:
                        diverging_counts[num_diverging]["dataexposer"].append(dataexposer_inter)
                        # diverging_counts[num_diverging]["bugdoc"].append(bugdoc_inter)
                        # diverging_counts[num_diverging]["anchor"].append(anchor_inter)
                        diverging_counts[num_diverging]["grptest"].append(grptest_inter)

                diverging_horizontal = sorted(list(diverging_counts.keys()))
                attributes_horizontal = sorted(list(attribute_counts.keys()))
                diverging_horizontal_time_dict[pvt][t] = diverging_horizontal
                attributes_horizontal_time_dict[pvt][t] = attributes_horizontal

                exposer_attr = [np.mean(attribute_counts[count]['dataexposer']) for count in attributes_horizontal]
                # bugdoc_attr = [np.mean(attribute_counts[count]['bugdoc']) for count in attributes_horizontal]
                # anchor_attr = [np.mean(attribute_counts[count]['anchor']) for count in attributes_horizontal]
                grptest_attr = [np.mean(attribute_counts[count]['grptest']) for count in attributes_horizontal]
                exposer_attr_time_dict[pvt][t] = exposer_attr
                # bugdoc_attr = %s" % (str(bugdoc_attr)))
                # anchor_attr = %s" % (str(anchor_attr)))
                gt_attr_time_dict[pvt][t] = grptest_attr

                exposer_diverging = [np.mean(diverging_counts[count]['dataexposer']) for count in diverging_horizontal]
                # bugdoc_diverging = [np.mean(diverging_counts[count]['bugdoc']) for count in diverging_horizontal]
                # anchor_diverging = [np.mean(diverging_counts[count]['anchor']) for count in diverging_horizontal]
                grptest_diverging = [np.mean(diverging_counts[count]['grptest']) for count in diverging_horizontal]
                exposer_diverging_time_dict[pvt][t] = exposer_diverging
                # bugdoc_diverging_time = %s" % (str(bugdoc_diverging)))
                # anchor_diverging_time = %s" % (str(anchor_diverging)))
                gt_diverging_time_dict[pvt][t] = grptest_diverging
            else:
                horizontal = []
                exposer = []
                bugdoc = []
                anchor = []
                grptest = []
                experiments = open("./SIGMOD_%s%s_%d/list.txt"% (c, "" if "domain" in pvt else "_missing",  t), 'r')
                examples = experiments.readlines()
                experiments.close()
                for e in examples:

                    if "conjunctions" in c:
                        horizontal.append(int(e.split('_')[7 if "missing" in pvt else 6]))
                    else:
                        horizontal.append(int(e.split('_')[6 if "missing" in pvt else 5]))

                    if os.path.exists(os.path.join(e.strip(), "pipeline_transform_200.adb")):
                        f = open(os.path.join(e.strip(), "pipeline_transform_200.adb"), 'r')
                        experiment_lines = f.readlines()
                        f.close()
                        bugdoc_inter = len(experiment_lines)
                    else:
                        bugdoc_inter = 0

                    if os.path.exists(os.path.join(e.strip(), "dp.txt")):
                        f = open(os.path.join(e.strip(), "dp.txt"), 'r')
                        experiment_lines = f.readlines()
                        f.close()
                        dataexposer_inter = int(experiment_lines[-1].strip())
                    else:
                        dataexposer_inter = 0
                    
                    if os.path.exists(os.path.join(e.strip(), "grptest.txt")):
                        f = open(os.path.join(e.strip(), "grptest.txt"), 'r')
                        experiment_lines = f.readlines()
                        f.close()
                        grptest_inter = int(experiment_lines[-1].strip())
                    else:
                        grptest_inter = 0
                    if os.path.exists(os.path.join(e.strip(), "anchor.txt")):
                        f = open(os.path.join(e.strip(), "anchor.txt"), 'r')
                        experiment_lines = f.readlines()
                        f.close()
                    else:
                        experiment_lines = []
                    anchor_inter = 0
                    for line in experiment_lines:
                        if "[" in line:
                            anchor_inter += 1

                    exposer.append(dataexposer_inter)
                    bugdoc.append(bugdoc_inter)
                    anchor.append(anchor_inter)
                    grptest.append(grptest_inter)

                horizontal_dict[c][pvt][t] = horizontal

                exposer_dict[c][pvt][t] = exposer
                bugdoc_dict[c][pvt][t] = bugdoc
                anchor_dict[c][pvt][t] = anchor
                gt_dict[c][pvt][t] = grptest

for e in ["domain"]: #["domain", "missing"]:

    for t in [2]: #[2, 4, 8, 16, 32]:
 
        _ , (ax1, ax2, ax3, ax4) = plt.subplots(1, 4,figsize=(12, 2.5), sharey=True)

        ax1.scatter(attributes_horizontal_dict[e][t], exposer_attr_dict[e][t], color='#1f77b4', marker='s', s=12, label='DataExposer$_{GRD}$')
        ax1.scatter(attributes_horizontal_dict[e][t], bugdoc_attr_dict[e][t], color='#ff7f0e', marker='o', s=12,label='BugDoc')
        ax1.scatter(attributes_horizontal_dict[e][t], anchor_attr_dict[e][t], color='#2ca02c', marker='^', s=12,label='Anchors')
        ax1.scatter(attributes_horizontal_dict[e][t], gt_attr_dict[e][t], color='#FF0000', marker='x', s=12,label='GrpTest')
        ax1.set_xlabel('(a) #Attributes')
        ax1.set_ylabel('Avg #Interventions')
        ax1.set_yscale('log')
        ax1.label_outer()

        ax2.scatter(diverging_horizontal_dict[e][t], exposer_diverging_dict[e][t], color='#1f77b4', marker='s', s=12, label='DataExposer$_{GRD}$')
        ax2.scatter(diverging_horizontal_dict[e][t], bugdoc_diverging_dict[e][t], color='#ff7f0e', marker='o', s=12,label='BugDoc')
        ax2.scatter(diverging_horizontal_dict[e][t], anchor_diverging_dict[e][t], color='#2ca02c', marker='^', s=12,label='Anchors')
        ax2.scatter(diverging_horizontal_dict[e][t], gt_diverging_dict[e][t], color='#FF0000', marker='x', s=12,label='GrpTest')
        #ax2.set_xticks(np.arange(16, 118, 25))
        #ax.set_yscale('log')
        ax2.set_xlabel('(b) #Discriminative PVTs')
        ax2.label_outer()



        #=========================================================================


        ax3.scatter(horizontal_dict['conjunctions'][e][t], exposer_dict['conjunctions'][e][t], color='#1f77b4', marker='s', s=12, label='DataExposer$_{GRD}$')
        ax3.scatter(horizontal_dict['conjunctions'][e][t], bugdoc_dict['conjunctions'][e][t], color='#ff7f0e', marker='o', s=12,label='BugDoc')
        ax3.scatter(horizontal_dict['conjunctions'][e][t], anchor_dict['conjunctions'][e][t], color='#2ca02c', marker='^', s=12,label='Anchors')
        ax3.scatter(horizontal_dict['conjunctions'][e][t], gt_dict['conjunctions'][e][t], color='#FF0000', marker='x', s=12,label='GrpTest')
        ax3.set_xlabel('(c) Size of Conjunction')
        ax3.label_outer()



        ax4.scatter(horizontal_dict['disjunctions'][e][t], exposer_dict['disjunctions'][e][t], color='#1f77b4', marker='s', s=12, label='DataExposer$_{GRD}$')
        ax4.scatter(horizontal_dict['disjunctions'][e][t], bugdoc_dict['disjunctions'][e][t], color='#ff7f0e', marker='o', s=12,label='BugDoc')
        ax4.scatter(horizontal_dict['disjunctions'][e][t], anchor_dict['disjunctions'][e][t], color='#2ca02c', marker='^', s=12,label='Anchors')
        ax4.scatter(horizontal_dict['disjunctions'][e][t], gt_dict['disjunctions'][e][t], color='#FF0000', marker='x', s=12,label='GrpTest')
        ax4.set_xlabel('(d) Size of Disjunction')
        ax4.label_outer()
        ax1.legend(loc='center', bbox_to_anchor=(0.1, 1.15), shadow=False, ncol=4)
        plt.tight_layout()
        plt.savefig("Figure8.pdf")



#=========================================================================
plt.figure(figsize=(6, 2.5))
ax = plt.subplot(1, 2, 1)
ax.scatter(attributes_horizontal_time[:], exposer_attr_time[:], color='#1f77b4', marker='s', s=12, label='DataExposer$_{GRD}$')
# ax.scatter(attributes_horizontal, bugdoc_attr, color='#ff7f0e', marker='o', s=12,label='BugDoc')
# ax.scatter(attributes_horizontal, anchor_attr, color='#2ca02c', marker='^', s=12,label='Anchor')
ax.scatter(attributes_horizontal_time[:], gt_attr_time[:], color='#FF0000', marker='x', s=12,label='GrpTest')
ax.set_xlabel('#Attributes')
ax.set_ylabel('Seconds')
ax.set_yscale('log')

ax = plt.subplot(1, 2, 2, sharey=ax)
ax.scatter(diverging_horizontal_time[:], exposer_diverging_time[:], color='#1f77b4', marker='s', s=12, label='DataExposer$_{GT}$')
# ax.scatter(diverging_horizontal, bugdoc_diverging, color='#ff7f0e', marker='o', s=12,label='BugDoc')
# ax.scatter(diverging_horizontal, anchor_diverging, color='#2ca02c', marker='^', s=12,label='Anchor')
ax.scatter(diverging_horizontal_time[:], gt_diverging_time[:], color='#FF0000', marker='x', s=12,label='GrpTest')
ax.set_xlabel('#Discriminative PVTs')
#ax.set_xticks(np.arange(16, 118, 25))
ax.set_yscale('log')
#ax.legend(loc='center', bbox_to_anchor=(0.1, 1.15), shadow=False, ncol=2)
plt.tight_layout()
plt.savefig("scalability.pdf")
#plt.show()



#==========================================================================

plt.figure()

data = [exposer_diverging_dict['domain'][2],
        exposer_diverging_dict['domain'][4],
        exposer_diverging_dict['domain'][8],
        exposer_diverging_dict['domain'][16],
        exposer_diverging_dict['domain'][32]]
labels = [2, 4, 8, 16, 32]

plt.boxplot(data, vert=True, patch_artist=True, labels=labels) 
plt.ylabel('# Interventions')
plt.title('(a) Domain')
plt.xlabel('Malfunction Thresholds')
plt.savefig('Figure9a.pdf')
#plt.show()


#==========================================================================
plt.figure()
data_missing = [exposer_diverging_dict['missing'][2],
        exposer_diverging_dict['missing'][4],
        exposer_diverging_dict['missing'][8],
        exposer_diverging_dict['missing'][16],
        exposer_diverging_dict['missing'][32]]
plt.boxplot(data_missing, vert=True, patch_artist=True, labels=labels) 
plt.ylabel('# Interventions')
plt.title('(b) Missing')
plt.xlabel('Malfunction Thresholds')
plt.yticks([0,2,4,6,8,10,12,14,16, 18])
plt.savefig('Figure9b.pdf')
#plt.show()



