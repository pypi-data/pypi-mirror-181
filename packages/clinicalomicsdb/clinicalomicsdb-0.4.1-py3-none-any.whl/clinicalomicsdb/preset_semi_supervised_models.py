""" ClinicalOmicsDB: Bridging the gap between next-generation clinical omics data and machine learning
Reference: Chang In Moon, Byron Jia, Bing Zhang
Paper link: TBD
Code author: Chang In Moon (moonchangin@gmail.com)
-----------------------------

preset_semi_supervised_models.py
- Train semi-supervised model and return predictions on the testing data

(1) stc_logit: self training logistic regression
(2) stc_xgb_model: self training XGBoost model
(3) stc_mlp: self training multi-layer perceptrons
(4) stc_svm: self training support vector machine classifier
(5) stc_knn: self training k-nearest neighbors classifier
(6) stc_rf: self training random forest classifier
(7) label_prop: Label propagation rbf kernel
(8) label_spread: Label spreading rbf kernel

"""

# Necessary packages
import pandas as pd 
import numpy as np
from sklearn.semi_supervised import LabelPropagation, LabelSpreading, SelfTrainingClassifier
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectPercentile, VarianceThreshold
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import check_pairwise_arrays, euclidean_distances

#%% 
def stc_logit(x_train, y_train, x_unlabel, x_test, parameters=None):
  """self training logistic regression.
  
  Args: 
    - x_train, y_train: training dataset
    - x_unlabel: unlabeled training dataset
    - x_test: testing feature
    - parameters: hyperparameter for optimization

  Returns:
    - y_test_hat: predicted values for x_test
  """
  # Define and fit model on training dataset
  if parameters != None:
      pipe = Pipeline([
      ('filter', VarianceThreshold()),
      ('kbest', SelectPercentile(percentile=20)),
      ('PCA', PCA(n_components = 10)),
      ('classifier', LogisticRegression(penalty='elasticnet', solver='saga', max_iter=10000, class_weight=True))
      ])
      model = GridSearchCV(pipe, parameters, scoring='roc_auc', cv=5, refit=True, n_jobs = 8, error_score=0)
      model.fit(x_train, y_train)
      self_training_model = SelfTrainingClassifier(model.best_estimator_, criterion = "threshold", max_iter = None, threshold = 0.6)
      X_train_mixed = pd.concat([x_train, x_unlabel])
      y_train_mixed = pd.concat([y_train, pd.Series([-1] * len(x_unlabel))])
      self_training_model.fit(X_train_mixed, y_train_mixed)
  elif parameters == None:    
      self_training_model = SelfTrainingClassifier(LogisticRegression(), criterion = "k_best", max_iter = None, threshold = 0.6)
      X_train_mixed = pd.concat([x_train, x_unlabel])
      y_train_mixed = pd.concat([y_train, pd.Series([-1] * len(x_unlabel))])
      self_training_model.fit(X_train_mixed, y_train_mixed)
  # Predict on x_test
  print(model.best_params_) 
  y_test_hat = self_training_model.predict_proba(x_test) 
  return y_test_hat

#%% 
def stc_xgb_model(x_train, y_train, x_unlabel, x_test, parameters=None):
  """self training XGBoost model
  
  Args: 
    - x_train, y_train: training dataset
    - x_unlabel: unlabeled training dataset
    - x_test: testing feature
    - parameters: hyperparameter for optimization

  Returns:
    - y_test_hat: predicted values for x_test
  """

  # Define and fit model on training dataset
  if parameters != None:
      pipe = Pipeline([
      ('filter', VarianceThreshold()),
      ('kbest', SelectPercentile(percentile=20)),
      ('PCA', PCA(n_components = 10)),
      ('classifier', xgb.XGBClassifier(verbosity = 0, silent=True, n_jobs = 8))
      ])
      model = GridSearchCV(pipe, parameters, scoring='roc_auc', cv=5, refit=True, n_jobs = 4, error_score=0)
      model.fit(x_train, y_train)
      self_training_model = SelfTrainingClassifier(model.best_estimator_, criterion = "threshold", max_iter = None, threshold = 0.6)
      X_train_mixed = pd.concat([x_train, x_unlabel])
      y_train_mixed = pd.concat([y_train, pd.Series([-1] * len(x_unlabel))])
      self_training_model.fit(X_train_mixed, y_train_mixed)
  elif parameters == None:
      self_training_model = SelfTrainingClassifier(xgb.XGBClassifier(verbosity = 0, silent=True, n_jobs = 8),
       criterion = "k_best", max_iter = None, threshold = 0.6)
      X_train_mixed = pd.concat([x_train, x_unlabel])
      y_train_mixed = pd.concat([y_train, pd.Series([-1] * len(x_unlabel))])
      self_training_model.fit(X_train_mixed, y_train_mixed)
  # Predict on x_test
  print(model.best_params_) 
  y_test_hat = self_training_model.predict_proba(x_test) 
  return y_test_hat


#%% 
def stc_mlp(x_train, y_train, x_unlabel, x_test, parameters=None):
  """self training multi-layer perceptrons
  
  Args: 
    - x_train, y_train: training dataset
    - x_unlabel: unlabeled training dataset
    - x_test: testing feature
    - parameters: hyperparameter for optimization

  Returns:
    - y_test_hat: predicted values for x_test
  """

  # Define and fit model on training dataset
  if parameters != None:
      pipe = Pipeline([
      ('filter', VarianceThreshold()),
      ('kbest', SelectPercentile(percentile=20)),
      ('PCA', PCA(n_components = 10)),
      ('classifier', MLPClassifier())
      ])
      model = GridSearchCV(pipe, parameters, scoring='roc_auc', cv=5, refit=True, n_jobs = 8, error_score=0)
      model.fit(x_train, y_train)
      self_training_model = SelfTrainingClassifier(model.best_estimator_, criterion = "threshold", max_iter = None, threshold = 0.6)
      X_train_mixed = pd.concat([x_train, x_unlabel])
      y_train_mixed = pd.concat([y_train, pd.Series([-1] * len(x_unlabel))])
      self_training_model.fit(X_train_mixed, y_train_mixed)
  elif parameters == None:
      self_training_model = SelfTrainingClassifier(MLPClassifier(),
       criterion = "k_best", max_iter = None, threshold = 0.6)
      X_train_mixed = pd.concat([x_train, x_unlabel])
      y_train_mixed = pd.concat([y_train, pd.Series([-1] * len(x_unlabel))])
      self_training_model.fit(X_train_mixed, y_train_mixed)
  # Predict on x_test
  print(model.best_params_) 
  y_test_hat = self_training_model.predict_proba(x_test) 
  return y_test_hat


#%% 
def stc_svm(x_train, y_train, x_unlabel, x_test, parameters=None):
  """self training support vector machine classifier
  
  Args: 
    - x_train, y_train: training dataset
    - x_unlabel: unlabeled training dataset
    - x_test: testing feature
    - parameters: hyperparameter for optimization

  Returns:
    - y_test_hat: predicted values for x_test
  """

  # Define and fit model on training dataset
  if parameters != None:
      pipe = Pipeline([
      ('filter', VarianceThreshold()),
      ('kbest', SelectPercentile(percentile=20)),
      ('PCA', PCA(n_components = 10)),
      ('classifier', SVC(probability = True))
      ])
      model = GridSearchCV(pipe, parameters, scoring='roc_auc', cv=5, refit=True, n_jobs = 8, error_score=0)
      model.fit(x_train, y_train)
      self_training_model = SelfTrainingClassifier(model.best_estimator_, criterion = "threshold", max_iter = None, threshold = 0.6)
      X_train_mixed = pd.concat([x_train, x_unlabel])
      y_train_mixed = pd.concat([y_train, pd.Series([-1] * len(x_unlabel))])
      self_training_model.fit(X_train_mixed, y_train_mixed)
  elif parameters == None:
      self_training_model = SelfTrainingClassifier(SVC(probability = True),
       criterion = "k_best", max_iter = None, threshold = 0.6)
      X_train_mixed = pd.concat([x_train, x_unlabel])
      y_train_mixed = pd.concat([y_train, pd.Series([-1] * len(x_unlabel))])
      self_training_model.fit(X_train_mixed, y_train_mixed)
  # Predict on x_test
  print(model.best_params_) 
  y_test_hat = self_training_model.predict_proba(x_test) 
  return y_test_hat
#%% 
def stc_knn(x_train, y_train, x_unlabel, x_test, parameters=None):
  """self training k-nearest neighbors classifier
  
  Args: 
    - x_train, y_train: training dataset
    - x_unlabel: unlabeled training dataset
    - x_test: testing feature
    - parameters: hyperparameter for optimization

  Returns:
    - y_test_hat: predicted values for x_test
  """

  # Define and fit model on training dataset
  if parameters != None:
      pipe = Pipeline([
      ('filter', VarianceThreshold()),
      ('kbest', SelectPercentile(percentile=20)),
      ('PCA', PCA(n_components = 10)),
      ('classifier', KNeighborsClassifier())
      ])
      model = GridSearchCV(pipe, parameters, scoring='roc_auc', cv=5, refit=True, n_jobs = 8, error_score=0)
      model.fit(x_train, y_train)
      self_training_model = SelfTrainingClassifier(model.best_estimator_, criterion = "threshold", max_iter = None, threshold = 0.6)
      X_train_mixed = pd.concat([x_train, x_unlabel])
      y_train_mixed = pd.concat([y_train, pd.Series([-1] * len(x_unlabel))])
      self_training_model.fit(X_train_mixed, y_train_mixed)
  elif parameters == None:
      self_training_model = SelfTrainingClassifier(KNeighborsClassifier(),
       criterion = "k_best", max_iter = None, threshold = 0.6)
      X_train_mixed = pd.concat([x_train, x_unlabel])
      y_train_mixed = pd.concat([y_train, pd.Series([-1] * len(x_unlabel))])
      self_training_model.fit(X_train_mixed, y_train_mixed)
  # Predict on x_test
  print(model.best_params_) 
  y_test_hat = self_training_model.predict_proba(x_test) 
  return y_test_hat

#%% 
def stc_rf(x_train, y_train, x_unlabel, x_test, parameters=None):
  """self training random forest
  
  Args: 
    - x_train, y_train: training dataset
    - x_unlabel: unlabeled training dataset
    - x_test: testing feature
    - parameters: hyperparameter for optimization

  Returns:
    - y_test_hat: predicted values for x_test
  """

  # Define and fit model on training dataset
  if parameters != None:
      pipe = Pipeline([
      ('filter', VarianceThreshold()),
      ('kbest', SelectPercentile(percentile=20)),
      ('PCA', PCA(n_components = 10)),
      ('classifier', RandomForestClassifier(n_jobs = 4))
      ])
      model = GridSearchCV(pipe, parameters, scoring='roc_auc', cv=5, refit=True, n_jobs = 8, error_score=0)
      model.fit(x_train, y_train)
      self_training_model = SelfTrainingClassifier(model.best_estimator_, criterion = "threshold", max_iter = None, threshold = 0.6)
      X_train_mixed = pd.concat([x_train, x_unlabel])
      y_train_mixed = pd.concat([y_train, pd.Series([-1] * len(x_unlabel))])
      self_training_model.fit(X_train_mixed, y_train_mixed)
  elif parameters == None:
      self_training_model = SelfTrainingClassifier(RandomForestClassifier(),
       criterion = "k_best", max_iter = None, threshold = 0.6)
      X_train_mixed = pd.concat([x_train, x_unlabel])
      y_train_mixed = pd.concat([y_train, pd.Series([-1] * len(x_unlabel))])
      self_training_model.fit(X_train_mixed, y_train_mixed)
  # Predict on x_test
  y_test_hat = self_training_model.predict_proba(x_test) 
  print(model.best_params_) 
  return y_test_hat  
#%% 
def label_prop(x_train, y_train, x_unlabel, x_test, parameters=None):
  """Label propagation RBF kernel
  
  Args: 
    - x_train, y_train: training dataset
    - x_unlabel: unlabeled training dataset
    - x_test: testing feature

  Returns:
    - y_test_hat: predicted values for x_test
  """
  pipe = Pipeline([
      ('filter', VarianceThreshold()),
      ('kbest', SelectPercentile(percentile=20)),
      ('PCA', PCA(n_components = 10)),
      ('classifier', LabelPropagation(kernel="rbf",
      max_iter=1000,
      gamma = 1e-3,
      tol=1e-3))
      ])
  model = GridSearchCV(pipe, parameters, scoring='roc_auc', cv=5, refit=True, n_jobs = 8, error_score=0)
  X_train_mixed = pd.concat([x_train, x_unlabel])
  y_train_mixed = pd.concat([y_train, pd.Series([-1] * len(x_unlabel))])
  model.fit(X_train_mixed, y_train_mixed)
  print(model.best_params_) 
  y_test_hat = model.predict_proba(x_test)
  return y_test_hat

#%% 
def label_spread(x_train, y_train, x_unlabel, x_test, parameters=None):
  """Label spreading RBF kernel
  
  Args: 
    - x_train, y_train: training dataset
    - x_unlabel: unlabeled training dataset
    - x_test: testing feature

  Returns:
    - y_test_hat: predicted values for x_test
  """
  pipe = Pipeline([
      ('filter', VarianceThreshold()),
      ('kbest', SelectPercentile(percentile=20)),
      ('PCA', PCA(n_components = 10)),
      ('classifier', LabelSpreading(kernel="rbf",
      alpha = 0.2,
      max_iter=1000,
      gamma = 1e-3,
      tol=1e-3))
      ])
  model = GridSearchCV(pipe, parameters, scoring='roc_auc', cv=5, refit=True, n_jobs = 8, error_score=0)
  X_train_mixed = pd.concat([x_train, x_unlabel])
  y_train_mixed = pd.concat([y_train, pd.Series([-1] * len(x_unlabel))])
  model.fit(X_train_mixed, y_train_mixed)
  print(model.best_params_) 
  y_test_hat = model.predict_proba(x_test)
  return y_test_hat