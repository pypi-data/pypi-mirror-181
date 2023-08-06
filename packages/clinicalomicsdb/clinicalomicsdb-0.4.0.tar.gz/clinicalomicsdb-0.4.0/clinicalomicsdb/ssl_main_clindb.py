""" ClinicalOmicsDB: Bridging the gap between next-generation clinical omics data and machine learning
Reference: Chang In Moon, Byron Jia, Bing Zhang
Paper link: TBD
Code author: Chang In Moon (moonchangin@gmail.com)
-----------------------------

USAGE:
# for running self training logistic and svm model across all clinicalomics databases over 10 monte carlo cross validations
$ python3 ssl_main_clindb.py --model_list stc_logit stc_svm --mc_split 10 

# for running logistic and svm model with breast cancer TNBC patient over 10 monte carlo cross validations
$ python3 ssl_main_clindb.py --model_list stc_logit stc_svm --mc_split 10 --subset BRCA_TNBC


output: list of database auroc or acc performance across databases
"""
# Necessary packages
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
#from importlib_metadata import files
from datetime import datetime
from re import A
import numpy as np
import pandas as pd
import os

from database_download import download, get_ssl_dataset_link, ssl_HR_dataset_link, ssl_HER2_dataset_link, ssl_TNBC_dataset_link
from sklearn.preprocessing import StandardScaler, MaxAbsScaler
from sklearn.model_selection import train_test_split
from preset_semi_supervised_models import stc_logit, stc_xgb_model, stc_mlp, stc_svm, stc_knn, stc_rf, label_prop, label_spread
from utils import perf_metric

# define and edit parameters for semi-supervised learning models
def semi_supervised_model_training (x_train, y_train, x_unlabel, x_test,
                               y_test, model_name, metric):
  """Train semi-supervised learning models and report the results.
  list of parameters will be definded in the function
  Args:
    - x_train, y_train: training dataset
    - x_test, y_test: testing dataset
    - model_name: stc_logit
    - metric: acc or auc

  Returns:
    - performance: prediction performance
  """

  # Train semi-supervised model w/ specified hyperparameters
  # Logistic regression
  if model_name == 'stc_logit':
    log_param = dict()
    log_param['kbest__percentile'] = [20, 100]
    log_param['classifier__l1_ratio'] = np.arange(0.1,1.1,0.2)
    log_param['classifier__C'] = np.logspace(-3,3,5)
    y_test_hat = stc_logit(x_train, y_train, x_unlabel, x_test, log_param)
  # XGBoost
  elif model_name == 'stc_xgb_model':
    xg_param = dict()
    xg_param['kbest__percentile'] = [20, 100]
    xg_param['classifier__max_depth'] = [4, 6, 8, 10]
    xg_param['classifier__n_estimators'] = range(100, 400, 100)
    xg_param['classifier__use_label_encoder'] = [False]
    xg_param['classifier__eval_metric'] = ["logloss"]
    y_test_hat = stc_xgb_model(x_train, y_train, x_unlabel, x_test, xg_param)
  # MLP
  elif model_name == 'stc_mlp':
    mlp_param = dict()
    mlp_param['kbest__percentile'] = [20, 100]
    mlp_param['classifier__hidden_layer_sizes'] = [(10,5)]
    mlp_param['classifier__activation'] = ['relu']
    mlp_param['classifier__solver'] = ['adam']
    mlp_param['classifier__max_iter'] = [5000]
    mlp_param['classifier__alpha'] = [0.0001, 0.05]
    mlp_param['classifier__learning_rate'] = ['constant','adaptive']
    y_test_hat = stc_mlp(x_train, y_train, x_unlabel, x_test, mlp_param)
  # SVM
  elif model_name == 'stc_svm':
    svm_param = dict()
    svm_param['kbest__percentile'] = [20, 100]
    svm_param['classifier__C'] = [0.001, 0.01, 0.1, 1, 10, 100]
    svm_param['classifier__gamma'] = [0.001, 0.01, 0.1, 1, 10, 100]
    y_test_hat = stc_svm(x_train, y_train, x_unlabel, x_test, svm_param)
  # KNN
  elif model_name == 'stc_knn':
    knn_param = dict()
    knn_param['kbest__percentile'] = [20, 100]
    knn_param['classifier__n_neighbors'] = range(1, 10, 1)
    knn_param['classifier__weights'] = ['uniform','distance']
    knn_param['classifier__p'] = [1,2]
    y_test_hat = stc_knn(x_train, y_train, x_unlabel, x_test, knn_param)
  # Random Forest
  elif model_name == 'stc_rf':
    rf_param = dict()
    rf_param['kbest__percentile'] = [20, 100]
    rf_param['classifier__max_depth'] = [4, 6, 8, 10]
    rf_param['classifier__n_estimators'] = range(100, 400, 100)
    y_test_hat = stc_rf(x_train, y_train, x_unlabel, x_test, rf_param)
  # Label propagation
  elif model_name == 'label_prop':
    prop_param = dict()
    prop_param['kbest__percentile'] = [20, 100]
    y_test_hat = label_prop(x_train, y_train, x_unlabel, x_test, prop_param)
  # Label spreading
  elif model_name == 'label_spread':
    spread_param = dict()
    spread_param['kbest__percentile'] = [20, 100]
    y_test_hat = label_spread(x_train, y_train, x_unlabel, x_test, spread_param)
  # User customized ML model
  # elif model_name == 'custom':
  #   custom_param = dict() # user must add in required parameters here
  #   custom_param['kbest__percentile'] = [100]
  # y_test_hat = custom(x_train, y_train, x_unlabel, x_test, custom_param) # user must create a customized function in "preset_semi_supervised_models.py"
  # Report the performance
  performance = perf_metric(metric, y_test, y_test_hat)
  return performance

def main(args):
  """Main function for benchmarking.
  
  Args:
    - mc_split: Number of monte carlo cross validation splits [default: 50]
    - model_name: List of ML model name e.g. [mlp, logit, or xgboost]
    - output: name of the output file [default: clinicalomicsdb_output.csv]
    - metric: acc or auc [default: auc]
    - user_data: data (X) input the user would like to independantly train on [optional;
     1st column: sample_name; 2nd column: response, 3rd+ column: other biomarkers]
    - user_label: label (y) input the user [optional; must match with data X samples]

  Returns:
    - a csv file with all performances of the models (supervised; semi-supervised; customized models etc...)
  """
  
  if args.subset == "all":
    collection = get_ssl_dataset_link()
  elif args.subset == "BRCA_HR":
    collection = ssl_HR_dataset_link()
  elif args.subset == "BRCA_HER2":
    collection = ssl_HER2_dataset_link()
  elif args.subset == "BRCA_TNBC":
    collection = ssl_TNBC_dataset_link()

  db_name = collection.iloc[:, 0]
  output_df = []
  # rest of the model method will be performed on all datasets
  for f in db_name:
      print("Training " + f)
      url = collection.loc[collection['Series'] == f]
      url = url.iloc[0,1]
      temp_df = download(url)      
      temp_df = temp_df.dropna(axis='columns') # Remove genes with missing values
      X = temp_df.iloc[:, 2:] # expression data only
      y = temp_df.iloc[:, 1] # Response is on 2nd column

      # identify parallel treatment arms
      unlabel_target = f.split("_")[1] 
      unlabel_list = collection[collection['Series'].str.contains(unlabel_target)]
      unlabel_list = unlabel_list.loc[unlabel_list['Series'] != f] # data frame
      url_list = unlabel_list.iloc[:,1] # list of urls
      unlabel_df = []
      for link in url_list:
          unlabel_df.append(download(link)) # merge unlabeled datasets together
      merged = pd.concat(unlabel_df, axis=0, ignore_index=True)
      X_unlabel = merged.iloc[:, 2:] # expression data only
      X_unlabel = X_unlabel.dropna(axis='columns') # Remove genes with missing values
      
      # match genes before entering ssl
      markers_1 = list(X.columns)
      markers_2 = list(X_unlabel.columns)
      markers = list(set(markers_1) & set(markers_2))
      X = X[X.columns.intersection(markers)]
      X_unlabel = X_unlabel[X_unlabel.columns.intersection(markers)]
  
      # Define semi-supervised model & inputs
      model_sets = args.model_list
      seed = 1
      while seed <= args.mc_split:
          # perform a stratified monte carlo cross validation (Here we will leave 20% of testing for final model evalutation)
          X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=seed, stratify=y)
          for m_it in range(len(model_sets)):
              model_name = model_sets[m_it]
              try:
                tmp = semi_supervised_model_training(X_train, y_train, X_unlabel, X_test, 
                                                        y_test, model_name, metric = args.metric)
              except Exception:
                print("Skipping " + f + " due to either small sample size or imbalanced labels")
                break # do not print or save results if the database have few positive labels or small sample size
              # parse file name
              database_name = f[10:]
              database_name = database_name[:-4]
              test_eval = {'dataset': database_name,
               'model': model_sets[m_it],
                'auroc': tmp,
                 'sample_size': X.shape[0],
                 'feature_size': X.shape[1],
                 'responder_log_ratio': round(abs(np.log(y.sum()/(len(y)-y.sum()))),2)
                 }
              print(test_eval)
              output_df.append(test_eval)
          seed += 1
  # save your final results
  df2 = pd.DataFrame(output_df)
  df2.to_csv(args.output)
  
if __name__ == '__main__':
  # Inputs for the main function
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '-l',
      '--model_list',
      help='list of ML model name (e.g. stc-logit stc-xgboost custom etc...)',
      nargs='+',
      required=True)  
  parser.add_argument(
      '--mc_split',
      help='number of monte carlo cross validation per database (default: 30)',
      default=30,
      type=int)
  parser.add_argument(
      '--output',
      help='name of the output file (default: clinicalomicsdb_output_[CURRENT_TIME].csv)',
      default="clinicalomicsdb_output_" + datetime.now().strftime("%H:%M:%S") + ".csv",
      type=str)
  parser.add_argument(
      '--metric',
      help='acc or auc (default: auc)',
      default="auc",
      type=str)
  parser.add_argument(
      '--subset',
      help='select particular subset of cohort for machine learning analysis (default: all) [available subset: BRCA_HR, BRCA_HER2, BRCA_TNBC]',
      default="all",
      type=str)
  args = parser.parse_args() 
  # Calls main function  
  main(args)