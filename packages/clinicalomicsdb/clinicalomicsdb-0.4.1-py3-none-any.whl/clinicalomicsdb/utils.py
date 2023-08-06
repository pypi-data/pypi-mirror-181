""" ClinicalOmicsDB: Bridging the gap between next-generation clinical omics data and machine learning
Reference: Chang In Moon. Byron Jia, Bing Zhang
Paper link: TBD
Code author: Chang In Moon (moonchangin@gmail.com)
-----------------------------

utils.py
- Various utility functions for ClinicalOmicsDB framework
(1) perf_metric: prediction performances in terms of AUROC or accuracy
"""

# Necessary packages
import numpy as np
from sklearn.metrics import accuracy_score, roc_auc_score

#%% 
def perf_metric (metric, y_test, y_test_hat):
  """Evaluate performance.
  
  Args:
    - metric: acc or auc
    - y_test: ground truth label
    - y_test_hat: predicted values
    
  Returns:
    - performance: Accuracy or AUROC performance
  """
  # Accuracy metric
  if metric == 'acc':
    if np.isnan(y_test_hat[:,1]).any() == True: # NaN predictions will be automatically be stored as 0
      result = 0
      return result
    result = accuracy_score(np.argmax(y_test, axis = 1), 
                            np.argmax(y_test_hat, axis = 1))
  # AUROC metric
  elif metric == 'auc':
    if np.isnan(y_test_hat[:,1]).any() == True: # NaN predictions will be automatically be stored as 0
      result = 0
      return result
    result = roc_auc_score(y_test, y_test_hat[:,1])
  return result
