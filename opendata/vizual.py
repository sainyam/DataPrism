import pandas as pd
import random
import math
from math import sin, cos, sqrt, atan2

R = 6373.0
def get_distance(i1,i2,df):

    r1=df.iloc[i1]
    r2=df.iloc[i2]
    a1=r1['Phone'][:3]
    lat1=r1['Latitude']
    long1=r1['Longitude']

    a2=r2['Phone'][:3]
    lat2=r2['Latitude']
    long2=r2['Longitude']


    dlon = long2 - long1
    dlat = lat2 - lat1
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c + abs(int(a1)-int(a2))

    
    return distance

def generate_clusters(clean_df,k):
	first_center=random.randint(0,clean_df.shape[0])
	assignment={}
	i=0
	while i<clean_df.shape[0]:
	    assignment[i]=0
	    i+=1
	    
	centers=[first_center]
	i=1
	while i<k:
	    max_dist=0
	    max_dist_j=-1
	    j=0
	    while j<clean_df.shape[0]:     
	        dist=get_distance(j,centers[assignment[j]],clean_df)
	        if dist>max_dist:
	            max_dist=dist
	            max_dist_j=j
	        j+=1
	    centers.append(max_dist_j)
	    
	    j=0
	    while j<clean_df.shape[0]:     
	        dist=get_distance(j,centers[-1],clean_df)
	        old_dist=get_distance(j,centers[assignment[j]],clean_df)
	        if dist<old_dist:
	            assignment[j]=len(centers)-1
	        j+=1
	    
	    
	    i+=1
	return centers

def test_clusters(df):

	try:
		center=generate_clusters(df,5)
		return 1
	except:
		return 0
if __name__ == "__main__":
	df=pd.read_csv('dirty.csv')
	generate_clusters(df,5)
