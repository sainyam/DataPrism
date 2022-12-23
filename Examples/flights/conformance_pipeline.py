#!/usr/bin/env python
# coding: utf-8

# In[30]:


import pandas as pd
import numpy as np
from sklearn import preprocessing
import prose.datainsights as di
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from scipy.stats.stats import pearsonr  
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import os
import sys
np.random.seed(0)

def run(data, threshold, bugs):
	train = pd.read_csv("Examples/flights/train.csv")
	test = pd.read_csv(data)

	y_train=train['ArrivalDelay']
	y_test=test['ArrivalDelay']
	train=train.drop(columns=["ArrivalDelay"])
	test=test.drop(columns=["ArrivalDelay"])

	reg = LinearRegression().fit(train, y_train)
	mae = mean_absolute_error(y_test, reg.predict(test))
	print(mae)

	return mae < threshold, 0

'''
def transformation(df):
    CRSArrivalTimecol=[]
    for index,row in df.iterrows():
        if row['CRSDepartureTime'] > row['CRSArrivalTime']:
            CRSArrivalTimecol.append(row['CRSArrivalTime']+24*60)
        else:
            CRSArrivalTimecol.append(row['CRSArrivalTime'])
    df['CRSArrivalTime']=CRSArrivalTimecol
    return df
''' 
