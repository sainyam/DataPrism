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

def train_classifier(test):
	train = pd.read_csv("../datasets/flights/train.csv")

	y_train=train['ArrivalDelay']
	y_test=test['ArrivalDelay']
	train=train.drop(columns=["ArrivalDelay"])
	test=test.drop(columns=["ArrivalDelay"])


	reg = LinearRegression().fit(train, y_train)

	return ( mean_absolute_error(y_test, reg.predict(test)))

