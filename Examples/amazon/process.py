f=open('clean.csv','r')

for line in f:
	line=line.strip()
	line=line.split(',')
	txt=line[0]+','+' '.join(line[1:])
	print(txt)
