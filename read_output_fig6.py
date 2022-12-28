import os

time={'dp':{}, 'bugdoc':{}, 'anchor':{}}
num_int={'dp':{}, 'bugdoc':{}, 'anchor':{}}
for folder in ['tweets','adult','bmi','flights','amazon','opendata','physicians']:
	if os.path.exists('./'+folder+'/dp.txt'):
		f=open('./'+folder+'/dp.txt')
		for line in f:
			line=line.strip().split()
			num_int['dp'][folder]=line[0]
			time['dp'][folder]=line[1]
		f.close()
	else:
		num_int['dp'][folder]=0
		time['dp'][folder]='N/A'

	if os.path.exists(os.path.join('./Examples',folder, "pipeline_transform_200.adb")):
		f = open(os.path.join('./Examples',folder,  "pipeline_transform_200.adb"), 'r')
		experiment_lines = f.readlines()
		f.close()
		num_int['bugdoc'][folder] = len(experiment_lines)
	else:
		num_int['bugdoc'][folder] = 0
	
	if os.path.exists(os.path.join('./Examples',folder, "pipeline_transform_200.result")):
		f = open(os.path.join('./Examples',folder,  "pipeline_transform_200.result"), 'r')
		experiment_lines = f.readlines()
		f.close()
		time['bugdoc'][folder] = experiment_lines[-1]
	else:
		time['bugdoc'][folder] = 'N/A'

	if os.path.exists(os.path.join('./Examples',folder, "anchors.txt")):
		f = open(os.path.join('./Examples',folder, "anchors.txt"), 'r')
		experiment_lines = f.readlines()
		f.close()
		time['anchor'][folder] = experiment_lines[-1]
	else:
		experiment_lines = []
		time['anchor'][folder] = 'N/A'

	num_int['anchor'][folder] = 0

	for line in experiment_lines:
	    if "[" in line:
	        num_int['anchor'][folder] += 1

print (time,'\n\n',num_int)

fout=open('freshRuns/fig6.txt',"w")
fout.write(time)
fout.write('\n\n')
fout.write(num_int)
fout.close()

