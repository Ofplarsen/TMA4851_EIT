import mat73
import scipy
import scipy.io as sio # cannot use for v7.3 mat file
import numpy as np
import signal_functions
import matplotlib.pyplot as plt
import pandas as pd

import signal_functions as sf

def Calibration(nontargetuse):
   '''
   find max amplitude from nontarget-data in interested interval, data should be from a calibration round
   returns max_nontarget for each electrode in an array
   '''
   avg_nontarget = np.mean(nontargetuse, axis=2) 
   max_nontarget = np.max(avg_nontarget, axis=1)
   return max_nontarget
#   max_eachtest_nontarget = np.max(nontargetuse, axis=1)
#   max_eachtest_target = np.max(targetuse, axis=1)
#   max_target = np.max(avg_target, axis=1)
   #max_target.append(np.average(max_eachtest_target))
#   for i in range(n):
#      max_eachtest_nontarget = np.max(nontargetuse[i,:], axis=0)
#      max_nontarget.append(np.average(max_eachtest_nontarget))
#      max_eachtest_target = np.max(targetuse[i,:], axis=0)
#      max_target.append(np.average(max_eachtest_target))


def ClassificationMaxAvg(max_nontarget, check, threshold):
   '''
   Return if a check-data can be classified as target
   '''
   avg_check = np.mean(check, axis=2) 
   max_check = np.max(avg_check, axis=1)
   b = max_check > max_nontarget
   percentage = np.sum(b)/len(b)
   print("Number of events", len(b))
   print("Percentage in classification", percentage)
   if percentage >= threshold:
      return True
   else:
      return False

nontargetuse, targetuse, nosortuse = sf.ReadFile("test_data/s52.mat", 8, 250, 450)
print(nosortuse.shape)
max_nontarget = Calibration(nontargetuse)
ClassificationMaxAvg(max_nontarget, targetuse, 0.63212)
print('Now beore sorting based on target/no target, 8 electrodes')
ClassificationMaxAvg(max_nontarget, nosortuse, 0.63212)
sf.plotdata(250, 450, nosortuse, nontargetuse, 8)
# GeneralizedCheck():