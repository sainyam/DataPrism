time={}
num_int={}
for folder in ['tweets','adult','bmi','flights','amazon','opendata','physicians']:
	f=open('./'+folder+'/dp.txt')
	for line in f:
		line=line.strip().split()
		num_int[folder]=line[0]
		time[folder]=line[1]

print (time,num_int)
