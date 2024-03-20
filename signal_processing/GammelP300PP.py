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
   max_check = np.max(check, axis=2)  #Average over all non-target events; TODO: check if possible to do max over all events then pick out avg
   peak = np.max(max_check[:, 200:], axis=1) - np.min(max_check[:, 0:200], axis=1)
   '''
   #If a negative answer, the find the peak using the event periode
   if np.min(peak) <= 0:
      peak = np.max(max_check[:, 220:500], axis=1) - np.min(max_check[:, 220:500], axis=1)
   else:
      pass
   '''
   print("non-target peak list:", peak)
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
      if peak_nontarget[electrode] < amp:
         TargetElectrode += 1
      else:
         continue
   b = TargetElectrode/n
   #print("percentage positive electrodes", b, "Event number", j)
   if b > threshold:
      return True
   else:
      return False
   
nontargetuse, targetuse, nosortuse, tgtpercentage = sf.ReadFile("data/s01.mat", 32, 220, 500)

ntp = MakePeak(nontargetuse)
print("target percentage", tgtpercentage)
#print(ClassificationWithPeak(ntp, nosortuse, 0.6, 32, 1))   #This is only one classification

#Now check percentage correct classification
def CheckClassPercentage(nontarget, nosort, threshold, n):
   '''
   nontarget: data array for non-target events
   nosort: data array not sorted after label
   threshold: the percentage of electrodes that needs to be positive to conclude a target event
   n: number of electrodes
   '''
   correct = 0
   for i in range(nosort.shape[2]):
      if ClassificationWithPeak(nontarget, nosort, threshold, n, i):
         correct += 1
   cp = correct/nosort.shape[2]
   return cp/tgtpercentage

#print("percentage correct classification", CheckClassPercentage(ntp, nosortuse, 0.752, 32))

def OptimizeThreshold(nontarget, nosort, n):
   '''
   nontarget: data array for non-target events
   nosort: data array not sorted after label
   n: number of electrodes
   '''
   threshold = np.linspace(0.6, 0.99, 60)
   percentage = []
   print("Running optimization")
   for t in threshold:
      perc = CheckClassPercentage(nontarget, nosort, t, n)
      if perc < 1:
         percentage.append(perc)
      else:
         percentage.append(0)

   for p in percentage:
      if p == max(percentage):
         index = percentage.index(p)
   return threshold[index]

#print("Optimal threshold", OptimizeThreshold(ntp, nosortuse, 32))

#optimal threshold = 0.752

def Test():
   nontargetuse, _, nosortuse, tgtpercentage = sf.ReadFileTest("data/s01.mat", 32, 220, 500)
   ntp = MakePeak(nontargetuse)
   print("target percentage", tgtpercentage)
   print(ClassificationWithPeak(ntp, nosortuse, 0.877, 32, 1))   #This is only one classification
   print("percentage correct classification", CheckClassPercentage(ntp, nosortuse, 0.752, 32))
#Test()