import os

time={'dp':{}, 'nog':{}, 'nb':{}}
num_int={'dp':{}, 'nog':{}, 'nb':{}}
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
	if os.path.exists('./'+folder+'/nog.txt'):
		f=open('./'+folder+'/nog.txt')
		for line in f:
			line=line.strip().split()
			num_int['nog'][folder]=line[0]
		f.close()
	else:
		num_int['nog'][folder]=0
	if os.path.exists('./'+folder+'/nb.txt'):
		f=open('./'+folder+'/nb.txt')
		for line in f:
			line=line.strip().split()
			num_int['nb'][folder]=line[0]
		f.close()
	else:
		num_int['nb'][folder]=0


print (num_int)


