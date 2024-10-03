# -*- coding: utf-8 -*-
"""flask7.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1u9q-LvqqBegNYZqoImZfCDiPSy2ThIkJ

<p style="text-align:center;">
    <font face="Georgia" size=5 color="red"><b>Import Required libraries</b></font>
</p>
"""

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split ,GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import SelectKBest, f_classif
import xgboost
from xgboost import XGBClassifier
import xgboost as xgb
import joblib
import numpy as np
from sklearn.preprocessing import MinMaxScaler

"""<p style="text-align:center;">
    <font face="Georgia" size=5 color="red"><b>Load Dataset</b></font>
</p>
"""

data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target
df

"""<p style="text-align:center;">
    <font face="Georgia" size=5 color="red"><b>Dataset Overview</b></font>
</p>
"""

df.info()

df.columns

"""<p style="text-align:center;">
    <font face="Georgia" size=5 color="red"><b>Feature Selection SELECTBEST</b></font>
</p>
"""

X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target
selector = SelectKBest(f_classif, k=10)
X_new = selector.fit_transform(X,y)
selected_features = X.columns[selector.get_support()]
print(selected_features.tolist())

selected_features = [
    'mean radius', 'mean perimeter', 'mean area', 'mean concavity', 'mean concave points',
    'worst radius', 'worst perimeter', 'worst area', 'worst concavity', 'worst concave points'
                    ]

"""<p style="text-align:center;">
    <font face="Georgia" size=5 color="red"><b> Min & Max</b></font>
</p>
"""

for feature in selected_features:
    min_value = df[feature].min()
    max_value = df[feature].max()
    print(f"Feature: {feature}, Min: {min_value:.2f}, Max: {max_value:.2f}")

"""<p style="text-align:center;">
    <font face="Georgia" size=5 color="red"><b> Model making</b></font>
</p>
"""

X = df[selected_features]
y = data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = xgb.XGBClassifier(eval_metric='logloss')
model.fit(X_train, y_train)

"""<p style="text-align:center;">
    <font face="Georgia" size=5 color="red"><b> Important point</b></font>
</p>

Model XGBoots is resistant to data not being scaled, and according to the test that was done, no difference in accuracy was created by using data scaling, and because of this, the data was not standardized.
"""

# scaler_X = MinMaxScaler()
# X_train_normalized = scaler_X.fit_transform(X_train)
# X_test_normalized = scaler_X.transform(X_test)

"""<p style="text-align:center;">
    <font face="Georgia" size=5 color="red"><b>Evaluation</b></font>
</p>
"""

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(accuracy * 100)

"""<p style="text-align:center;">
    <font face="Georgia" size=5 color="red"><b>Using GridSearch to increase accuracy</b></font>
</p>
"""

xgb = XGBClassifier( eval_metric='logloss', random_state=42)
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 4, 5, 6],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'subsample': [0.6, 0.8, 1.0],
    'colsample_bytree': [0.6, 0.8, 1.0],
    'gamma': [0, 0.1, 0.2, 0.3],
    'min_child_weight': [1, 3, 5]
}

grid_search = GridSearchCV(estimator=xgb, param_grid=param_grid,
                           scoring='accuracy', n_jobs=-1, cv=5, verbose=2)

grid_search.fit(X_train, y_train)
print("Best Parameters: ", grid_search.best_params_)
print("Best Accuracy: ", grid_search.best_score_)

"""<p style="text-align:center;">
    <font face="Georgia" size=5 color="red"><b>Rebuilding the model with the best parameters</b></font>
</p>
"""

best_xgb_model = XGBClassifier(
    colsample_bytree=0.6,
    gamma=0,
    learning_rate=0.01,
    max_depth=4,
    min_child_weight=1,
    n_estimators=300,
    subsample=0.8,
    eval_metric='logloss',
    random_state=42
)
best_xgb_model.fit(X_train, y_train)

"""<p style="text-align:center;">
    <font face="Georgia" size=5 color="red"><b>Evaluation</b></font>
</p>


"""

y_pred = best_xgb_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy on test data: {accuracy * 100:.2f}%")

"""<p style="text-align:center;">
    <font face="Georgia" size=5 color="red"><b>Save  model</b></font>
</p>
"""

joblib.dump(best_xgb_model, "model.pkl")
print("Model saved successfully.")