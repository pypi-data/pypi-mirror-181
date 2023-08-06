""" ClinicalOmicsDB: Bridging the gap between next-generation clinical omics data and machine learning
Reference: Chang In Moon, Byron Jia, Bing Zhang
Paper link: TBD
Code author: Chang In Moon (moonchangin@gmail.com)
-----------------------------

preset_supervised_models.py
- Collection of preset supervised models and return predicted labels for testing dataset
- This include a pipeline that can use preprocessing and feature selection as a hyperparameter
- Users may create a custom function in order to modify and test out their modified algorithms

(0) custom: user defined classifier

(1) logit: logistic regression
Source: Sammut, SJ Nature (2021)

(2) xgb_model: XGBoost model
Source: Shi, Z Molecular cellular proteomics (2021)

(3) mlp: multi-layer perceptron
Source: https://michael-fuchs-python.netlify.app/2021/02/03/nn-multi-layer-perceptron-classifier-mlpclassifier/

(4) svm: support vector machine classifier
Source: Shi, Z Molecular cellular proteomics (2021)

(5) knn: k-nearest neighbors classifier
Source: https://www.kaggle.com/code/abhinavdevarajan/breast-cancer-analysis-with-hyper-parameter-tuning

(6) rf: random forest classifier
Source: Shi, Z Molecular cellular proteomics (2021)

"""

# Necessary packages
from sklearn.linear_model import LogisticRegression # Logistic Reg (L2)
import xgboost as xgb #xgboost
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC # SVM
from sklearn.neighbors import KNeighborsClassifier # KNN
from sklearn.ensemble import RandomForestClassifier # Random Forest
from sklearn.tree import DecisionTreeClassifier # decision tree for custom algorithm
from sklearn.feature_selection import SelectPercentile, VarianceThreshold
from sklearn.model_selection import GridSearchCV 
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA

# %%
def custom(x_train, y_train, x_test, parameters=None):
  """Custom Classifier Specified by the user
  Feel free to customize this function that can return a y_test_hat (probability) at the end of the function.
  
  Args: 
    - x_train, y_train: training dataset
    - x_test: testing feature
    - parameters: hyperparameter for optimization
    
  Returns:
    - y_test_hat: predicted values for x_test
  """  
  if parameters != None:
      pipe = Pipeline([
      ('filter', VarianceThreshold()),
      ('kbest', SelectPercentile(percentile=20)),
      ('PCA', PCA(n_components = 10)),
      ('classifier', DecisionTreeClassifier())
      ])
      model = GridSearchCV(pipe, parameters, scoring='roc_auc', cv=5, refit=True, n_jobs = 8, error_score=0)
      model.fit(x_train, y_train)
  elif parameters == None:    
      model = DecisionTreeClassifier()
      model.fit(x_train, y_train)  
  print(model.best_params_) 
  y_test_hat = model.predict_proba(x_test)
  return y_test_hat

#%% 
def logit(x_train, y_train, x_test, parameters=None):
  """Logistic Regression.
  
  Args: 
    - x_train, y_train: training dataset
    - x_test: testing feature
    - parameters: hyperparameter for optimization

  Returns:
    - y_test_hat: predicted values for x_test
  """
  if parameters != None:
      pipe = Pipeline([
      ('filter', VarianceThreshold()),
      ('kbest', SelectPercentile(percentile=20)),
      ('PCA', PCA(n_components = 10)),
      ('classifier', LogisticRegression(penalty='elasticnet', solver='saga', max_iter=10000, class_weight=True))
      ])
      model = GridSearchCV(pipe, parameters, scoring='roc_auc', cv=5, refit=True, n_jobs = 8, error_score=0)
      model.fit(x_train, y_train)
  elif parameters == None:    
      model = LogisticRegression()
      model.fit(x_train, y_train)
  print(model.best_params_)
  y_test_hat = model.predict_proba(x_test) 
  return y_test_hat
#%% 
def xgb_model(x_train, y_train, x_test, parameters=None):
  """XGBoost.
  
  Args: 
    - x_train, y_train: training dataset
    - x_test: testing feature
    - parameters: hyperparameter for optimization

  Returns:
    - y_test_hat: predicted values for x_test
  """  
  if parameters != None:
      pipe = Pipeline([
      ('filter', VarianceThreshold()),
      ('kbest', SelectPercentile(percentile=20)),
      ('PCA', PCA(n_components = 10)),
      ('classifier', xgb.XGBClassifier(verbosity = 0, silent=True, n_jobs = 4))
      ])
      model = GridSearchCV(pipe, parameters, scoring='roc_auc', cv=5, refit=True, n_jobs = 4, error_score=0)
      model.fit(x_train, y_train)
  elif parameters == None:    
      model = xgb.XGBClassifier(verbosity = 0, silent=True, n_jobs = 8)
      model.fit(x_train, y_train)
  print(model.best_params_) 
  y_test_hat = model.predict_proba(x_test) 
  return y_test_hat
#%% 
def mlp(x_train, y_train, x_test, parameters=None):
  """multi-layer perceptrons
  
  Args: 
    - x_train, y_train: training dataset
    - x_test: testing feature
    - parameters: hyperparameter for optimization

  Returns:
    - y_test_hat: predicted values for x_test
  """  
  if parameters != None:
      pipe = Pipeline([
      ('filter', VarianceThreshold()),
      ('kbest', SelectPercentile(percentile=20)),
      ('PCA', PCA(n_components = 10)),
      ('classifier', MLPClassifier())
      ])
      model = GridSearchCV(pipe, parameters, scoring='roc_auc', cv=5, refit=True, n_jobs = 8, error_score=0)
      model.fit(x_train, y_train)
  elif parameters == None: 
      model = MLPClassifier()   
      model.fit(x_train, y_train)
  print(model.best_params_) 
  y_test_hat = model.predict_proba(x_test)
  return y_test_hat
#%% 
def svm(x_train, y_train, x_test, parameters=None):
  """support vector machine classifier
  
  Args: 
    - x_train, y_train: training dataset
    - x_test: testing feature
    - parameters: hyperparameter for optimization
    
  Returns:
    - y_test_hat: predicted values for x_test
  """  
  if parameters != None:
      pipe = Pipeline([
      ('filter', VarianceThreshold()),
      ('kbest', SelectPercentile(percentile=20)),
      ('PCA', PCA(n_components = 10)),
      ('classifier', SVC(probability=True))
      ])
      model = GridSearchCV(pipe, parameters, scoring='roc_auc', cv=5, refit=True, n_jobs = 8, error_score=0)
      model.fit(x_train, y_train)
  elif parameters == None: 
      model = SVC(probability = True)
      model.fit(x_train, y_train)
  print(model.best_params_) 
  y_test_hat = model.predict_proba(x_test)
  return y_test_hat
# %%
def knn(x_train, y_train, x_test, parameters=None):
  """k-nearest neighbors classifier
  
  Args: 
    - x_train, y_train: training dataset
    - x_test: testing feature
    - parameters: hyperparameter for optimization
    
  Returns:
    - y_test_hat: predicted values for x_test
  """  
  if parameters != None:
      pipe = Pipeline([
      ('filter', VarianceThreshold()),
      ('kbest', SelectPercentile(percentile=20)),
      ('PCA', PCA(n_components = 10)),
      ('classifier', KNeighborsClassifier())
      ])
      model = GridSearchCV(pipe, parameters, scoring='roc_auc', cv=5, refit=True, n_jobs = 8, error_score=0)
      model.fit(x_train, y_train)
  elif parameters == None:    
      model = KNeighborsClassifier()
      model.fit(x_train, y_train)
  print(model.best_params_) 
  y_test_hat = model.predict_proba(x_test)
  return y_test_hat
# %%
def rf(x_train, y_train, x_test, parameters=None):
  """Random Forest Classifier
  
  Args: 
    - x_train, y_train: training dataset
    - x_test: testing feature
    - parameters: hyperparameter for optimization
    
  Returns:
    - y_test_hat: predicted values for x_test
  """  
  if parameters != None:
      pipe = Pipeline([
      ('filter', VarianceThreshold()),
      ('kbest', SelectPercentile(percentile=20)),
      ('PCA', PCA(n_components = 10)),
      ('classifier', RandomForestClassifier(n_jobs = 4))
      ])
      model = GridSearchCV(pipe, parameters, scoring='roc_auc', cv=5, refit=True, n_jobs = 4, error_score=0)
      model.fit(x_train, y_train)
  elif parameters == None:    
      model = RandomForestClassifier(n_jobs = 4)
      model.fit(x_train, y_train)  
  print(model.best_params_) 
  y_test_hat = model.predict_proba(x_test) 
  return y_test_hat