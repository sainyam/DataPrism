import matplotlib.pyplot as plt
import matplotlib
import  numpy as np
from matplotlib.ticker import MaxNLocator
from matplotlib.font_manager import FontProperties



diverging_horizontal = [19, 23, 28, 37, 44, 66, 78, 87, 105, 108]
attributes_horizontal = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
exposer_attr = [2.0, 2.0, 3.0, 1.0, 1.0, 1.0, 7.0, 6.0, 12.0, 6.0]
bugdoc_attr = [18.0, 22.0, 30.0, 38.0, 46.0, 62.0, 70.0, 82.0, 98.0, 102.0]
anchor_attr = [448.0, 4863.0, 3878.0, 5702.0, 2303.0, 13774.0, 11703.0, 4503.0, 28291.0, 3903.0]
gt_attr = [4.0, 5.0, 5.0, 5.0, 5.0, 6.0, 6.0, 6.0, 6.0, 7.0]
exposer_diverging = [2.0, 2.0, 3.0, 1.0, 1.0, 1.0, 7.0, 6.0, 6.0, 12.0]
bugdoc_diverging = [18.0, 22.0, 30.0, 38.0, 46.0, 62.0, 70.0, 82.0, 102.0, 98.0]
anchor_diverging = [448.0, 4863.0, 3878.0, 5702.0, 2303.0, 13774.0, 11703.0, 4503.0, 3903.0, 28291.0]
gt_diverging = [4.0, 5.0, 5.0, 5.0, 5.0, 6.0, 6.0, 6.0, 7.0, 6.0]
conjunctions_horizontal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
exposer_conjunctions = [5, 1, 1, 1, 1, 1, 2, 1, 1, 1]
bugdoc_conjunctions = [200, 200, 200, 200, 200, 200, 200, 200, 200, 200]
anchor_conjunctions = [1903, 4103, 2103, 1103, 903, 2703, 703, 2303, 903, 1103]
gt_conjunctions = [11, 13, 11, 13, 11, 11, 9, 12, 9, 9]
disjunctions_horizontal = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
exposer_disjunctions = [3, 1, 1, 1, 10, 1, 4, 18, 4, 18]
bugdoc_disjunctions = [132, 126, 126, 130, 130, 128, 128, 124, 126, 124]
anchor_disjunctions = [500503, 471372, 479972, 502703, 565703, 528303, 566903, 462766, 416966, 416966]
gt_disjunctions = [77, 24, 149, 149, 298, 298, 298, 149, 298, 298]
diverging_horizontal_time = [69, 1853, 6157, 12804, 22199, 33746, 48216, 65069, 84225, 106082, 130432, 157071, 186566, 217744, 252107, 288754, 329347, 370388]
attributes_horizontal_time = [10, 60, 110, 160, 210, 260, 310, 360, 410, 460, 510, 560, 610, 660, 710, 760, 810, 860]
exposer_attr_time = [0.029430866241455078, 0.7266449928283691, 3.234330177307129, 4.886771202087402, 13.783616065979004, 9.70192003250122, 28.15203595161438, 24.933053016662598, 104.19999694824219, 38.69125509262085, 30.80706810951233, 236.8483488559723, 425.32921290397644, 52.220191955566406, 497.4534101486206, 694.9491801261902, 15332.690306186676, 19598.287848234177]
gt_attr_time = [0.16323471069335938, 0.9372751712799072, 2.322911024093628, 5.261242866516113, 7.595234632492065, 12.380239009857178, 18.48108410835266, 24.965620040893555, 31.865647077560425, 53.49918603897095, 66.77600812911987, 80.55005288124084, 87.90629506111145, 104.62124395370483, 103.66580986976624, 138.5898938179016, 117.04100513458252, 184.0877969264984]
exposer_diverging_time = [0.029430866241455078, 0.7266449928283691, 3.234330177307129, 4.886771202087402, 13.783616065979004, 9.70192003250122, 28.15203595161438, 24.933053016662598, 104.19999694824219, 38.69125509262085, 30.80706810951233, 236.8483488559723, 425.32921290397644, 52.220191955566406, 497.4534101486206, 694.9491801261902, 15332.690306186676, 19598.287848234177]
gt_diverging_time = [0.16323471069335938, 0.9372751712799072, 2.322911024093628, 5.261242866516113, 7.595234632492065, 12.380239009857178, 18.48108410835266, 24.965620040893555, 31.865647077560425, 53.49918603897095, 66.77600812911987, 80.55005288124084, 87.90629506111145, 104.62124395370483, 103.66580986976624, 138.5898938179016, 117.04100513458252, 184.0877969264984]




_ , (ax1, ax2, ax3, ax4) = plt.subplots(1, 4,figsize=(12, 2.5), sharey=True)

ax1.scatter(attributes_horizontal, exposer_attr, color='#1f77b4', marker='s', s=12, label='DataExposer$_{GRD}$')
ax1.scatter(attributes_horizontal, bugdoc_attr, color='#ff7f0e', marker='o', s=12,label='BugDoc')
ax1.scatter(attributes_horizontal, anchor_attr, color='#2ca02c', marker='^', s=12,label='Anchor')
ax1.scatter(attributes_horizontal, gt_attr, color='#FF0000', marker='x', s=12,label='GrpTest')
ax1.set_xlabel('(a) #Attributes')
ax1.set_ylabel('Avg #Interventions')
ax1.set_yscale('log')
ax1.label_outer()

ax2.scatter(diverging_horizontal, exposer_diverging, color='#1f77b4', marker='s', s=12, label='DataExposer$_{GRD}$')
ax2.scatter(diverging_horizontal, bugdoc_diverging, color='#ff7f0e', marker='o', s=12,label='BugDoc')
ax2.scatter(diverging_horizontal, anchor_diverging, color='#2ca02c', marker='^', s=12,label='Anchor')
ax2.scatter(diverging_horizontal, gt_diverging, color='#FF0000', marker='x', s=12,label='GrpTest')
#ax2.set_xticks(np.arange(16, 118, 25))
#ax.set_yscale('log')
ax2.set_xlabel('(b) #Discriminative PVTs')
ax2.label_outer()



#=========================================================================


ax3.scatter(conjunctions_horizontal, exposer_conjunctions, color='#1f77b4', marker='s', s=12, label='DataExposer$_{GRD}$')
ax3.scatter(conjunctions_horizontal, bugdoc_conjunctions, color='#ff7f0e', marker='o', s=12,label='BugDoc')
ax3.scatter(conjunctions_horizontal, anchor_conjunctions, color='#2ca02c', marker='^', s=12,label='Anchor')
ax3.scatter(conjunctions_horizontal, gt_conjunctions, color='#FF0000', marker='x', s=12,label='GrpTest')
ax3.set_xlabel('(c) Size of Conjunction')
ax3.label_outer()



ax4.scatter(disjunctions_horizontal, exposer_disjunctions, color='#1f77b4', marker='s', s=12, label='DataExposer$_{GRD}$')
ax4.scatter(disjunctions_horizontal, bugdoc_disjunctions, color='#ff7f0e', marker='o', s=12,label='BugDoc')
ax4.scatter(disjunctions_horizontal, anchor_disjunctions, color='#2ca02c', marker='^', s=12,label='Anchor')
ax4.scatter(disjunctions_horizontal, gt_disjunctions, color='#FF0000', marker='x', s=12,label='GrpTest')
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
