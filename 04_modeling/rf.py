
###
###  REF: https://www.datacamp.com/community/tutorials/random-forests-classifier-python
###  REF: https://stackabuse.com/random-forest-algorithm-with-python-and-scikit-learn/
###  REF: https://towardsdatascience.com/random-forest-in-python-24d0893d51c0
###
###
###  TODO: Further fit model. Tweak model.
###

import sklearn
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
import pandas
from sklearn import metrics
from sklearn.model_selection import train_test_split


###
###  Import folder path for flat CSV file.
###

from dotenv import load_dotenv
import os
load_dotenv()

ENV_HOME_PATH = os.getenv('FOLDER_PATH')

###
###  Load CSV data, print column names
###

imported_data = pandas.read_csv(ENV_HOME_PATH)

for col_name in imported_data.columns: 
    print(col_name)

###
###  Settings for random forest, if we want to change later on
###

# RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
#             max_depth=None, max_features='auto', max_leaf_nodes=None,
#             min_impurity_decrease=0.0, min_impurity_split=None,
#             min_samples_leaf=1, min_samples_split=2,
#             min_weight_fraction_leaf=0.0, n_estimators=100, n_jobs=1,
#             oob_score=False, random_state=None, verbose=0,
#             warm_start=False)

###
###  Choose predictors/features for model from imported CSV.
###

model_predictors = imported_data[['champExperience', 'timePlayed', 'totalDamageDealt', 'visionScore' , 'goldEarned']]

###
###  Choose outcome variable from imported CSV.
###

model_outcome = imported_data[['win']]

###
###  Create training/testing data sets.
###

X_train, X_test, y_train, y_test = train_test_split(model_predictors, model_outcome, test_size=0.3)


###
###  Input number of trees to randomly create.
###

clf=RandomForestClassifier(n_estimators=100)

###
###  Fit random forest
###

clf.fit(X_train,y_train.values.ravel())

###
###  Test predicted values
###

y_pred=clf.predict(X_test)
print(y_pred)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

###
###  Output most influential variables.
###

feature_imp = pandas.Series(clf.feature_importances_ , index = model_predictors.columns  ).sort_values(ascending=False)
print(feature_imp)