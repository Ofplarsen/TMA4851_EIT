import mat73
import scipy
import scipy.io as sio # cannot use for v7.3 mat file
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import signal_functions as sf

def MakePeak(check):
   '''
   Takes in electrode to analyze, return (max. amplitude - min. amplitude) after averaging over all events for one electrode
   '''
   avg_check = np.mean(check, axis=2)  #Average over all non-target events; TODO: check if possible to do max over all events then pick out avg
   peak = np.max(avg_check, axis=1) - np.min(avg_check, axis=1)
   print("non-target peak list?", peak)
   return peak

def ClassificationWithPeak(peak_nontarget, check, threshold, n, j):
   '''
   Peak_nontarget: must be obtained with non-target training set, a list, one peak for each electrode
   check: data array not sorted after label
   threshold: the percentage of electrodes that needs to be positive to conclude a target event
   j: specify the position of event in dataset
   '''
   TargetElectrode = 0
   for electrode in range(n):
      event_to_test = check[electrode,:,j]
      amp = np.max(event_to_test) - np.min(event_to_test)
      print("peak check:", amp, "electrode:", electrode)
      if peak_nontarget[electrode] < amp:
         TargetElectrode += 1
      else:
         continue
   b = TargetElectrode/n
   print("percentage positive electrodes", b)
   if b > threshold:
      return True
   else:
      return False
   
nontargetuse, targetuse, nosortuse, MarkerList = sf.ReadFile("../../data/s01.mat", 10, 220, 500)
ntp = MakePeak(nontargetuse)

#print(ClassificationWithPeak(ntp, nosortuse, 0.6, 10, 1))   #This is only one classification

print(len(nosortuse))
print(MarkerList.shape)

#TODO: sjekke mot labels