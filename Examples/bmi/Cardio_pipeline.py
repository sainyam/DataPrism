import pandas as pd
import os
from sklearn.model_selection import train_test_split



from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.ensemble import AdaBoostClassifier

from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import recall_score
def get_recall(data, threshold, bugs):
	test_df = pd.read_csv(data)
	mydir= os.path.dirname(data)
	train_df=pd.read_csv(os.path.join(mydir,'train.csv'))

	feat = test_df.columns
	train_df=train_df[feat]

	Xcol=list(train_df.columns)
	Xcol.remove('target')

	clf = AdaBoostClassifier(n_estimators=100, random_state=0)

	#clf = RandomForestClassifier(max_depth=10, random_state=0)
	clf.fit(train_df[Xcol], train_df['target'])



	y_pred=clf.predict(test_df[Xcol])
	out=(classification_report(test_df['target'], y_pred))
	score = recall_score(test_df['target'],y_pred, average=None)
	print(score[1])
	return score[1] > threshold, 0



