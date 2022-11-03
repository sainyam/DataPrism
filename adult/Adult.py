
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from collections import namedtuple, Counter
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, average_precision_score
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import pickle
from numpy import linalg
from sklearn.base import BaseEstimator
from sklearn.metrics.pairwise import rbf_kernel
#import multiprocessing
#from joblib import Parallel, delayed
from aif360.metrics import BinaryLabelDatasetMetric
from aif360.datasets import BinaryLabelDataset
from aif360.sklearn.metrics import disparate_impact_ratio, average_odds_error, generalized_fpr
import pandas as pd
from aif360.metrics import ClassificationMetric
from aif360.algorithms.preprocessing import Reweighing
from sklearn.ensemble import RandomForestClassifier
import copy
np.random.seed(101)


# In[2]:


def train_classifier(df,considered_feat,sensitive):
    
    X_train, X_test, y_train, y_test = train_test_split(df[considered_feat], df['target'], test_size=0.2, random_state=1)
    
    '''
    X_test=pd.read_csv('./data/adult/test.txt',delimiter=' ')
    y_test=X_test['target']
    X_test=X_test[considered_feat]
    
    X_train=df[considered_feat]
    y_train=df['target']
    '''
    
    model = RandomForestClassifier(max_depth=10, random_state=0)
    print(X_train)
    model.fit(X_train,y_train)
    print(model.feature_importances_)
    print(considered_feat)
    y_pred=model.predict(X_test)

    X_test['target']=y_test
    test = BinaryLabelDataset(df=X_test, label_names=['target'],protected_attribute_names=[sensitive])
    
    pred_df=copy.deepcopy(X_test)
    pred_df['target']=y_test
    dataset_pred = BinaryLabelDataset(df=pred_df, label_names=['target'],protected_attribute_names=[sensitive])

    privileged_groups = [{sensitive: 1}]
    unprivileged_groups = [{sensitive: 0}]

    dataset_pred.labels=y_pred
    metric_selection = ClassificationMetric(
                test, dataset_pred,
                unprivileged_groups=unprivileged_groups,
                privileged_groups=privileged_groups)

    #if metric_selection.disparate_impact():
    print("Disparate impact", metric_selection.disparate_impact())
    return metric_selection.disparate_impact()
    '''print ("Results")
    print("Odds difference",metric_selection.average_odds_difference())
    print("Disparate impact",metric_selection.disparate_impact())
    print(metric_selection.statistical_parity_difference())
    print(metric_selection.equal_opportunity_difference())
    print(metric_selection.theil_index())
    print ("Accuracy",metric_selection.accuracy())
    '''


# In[3]:


def run(data, threshold,bugs):
    df = pd.read_csv(data)  # ,delimiter=' ')
    considered_feat = list(df.columns)
    #considered_feat.remove('Unnamed: 15')
    considered_feat.remove('target')
    return train_classifier(df, considered_feat, 'sex') < threshold,0


if __name__ == "__main__":
    
    df=pd.read_csv('./Examples/adult/train.txt')#,delimiter=' ')
    considered_feat=list(df.columns)
    considered_feat.remove('Unnamed: 15')
    considered_feat.remove('target')
    
    print(df['target'].corr(df['sex']))
    print(train_classifier(df,considered_feat,'sex'))
    #df.to_csv('golddata_adult.csv',index=Fa)





