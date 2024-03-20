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
   #print("non-target peak list:", peak)
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
   
#print("target percentage", tgtpercentage)
#print("ntp:", ntp)
#print(ClassificationWithPeak(ntp, nosortuse, 0.6, 32, 1))   #This is only one classification

#Now check percentage correct classification
def CheckClassPercentage(ntp, nosort, threshold, n, marker):
   '''
   nontarget: data array for non-target events
   nosort: data array not sorted after label
   threshold: the percentage of electrodes that needs to be positive to conclude a target event
   n: number of electrodes
   '''
   correct = 0
   true = 0
   false = 0
   for i in range(len(nosort[0,0,:])):
      truetrue = len(np.where(marker==1)[0])*2
      truefalse = len(np.where(marker==2)[0])*2
      if ClassificationWithPeak(ntp, nosort, threshold, n, i):
         true += 1
         if i < 900:
            if marker[i] == 1:
               #print("Truetrue index found", i)
               correct += 1
         else:
            index = i - 900
            if marker[index] == 1:
               correct += 1
      else:
         false += 1
   #print('Known True false', truefalse)
   #print('Classified false', false)
   #print("Known True targets", truetrue)
   #print("Classified True targets", true)
   return correct/true

def OptimizeThresholdSimpel(nontarget, nosort, n):
   '''
   nontarget: data array for non-target events
   nosort: data array not sorted after label
   n: number of electrodes
   '''
   threshold = np.linspace(0.6, 0.99, 60)
   percentage = []
   print("Running optimization")
   for t in threshold:
      perc = CheckClassPercentage(nontarget, nosort, t, n, marker)
      if perc < 1:
         percentage.append(perc)
      else:
         percentage.append(0)

   for p in percentage:
      if p == max(percentage):
         index = percentage.index(p)
   return threshold[index]


def PerformaceElectrode(ntg, nosort, marker, e):
   '''
   return a list of best performing electrodes
   e: number of electrodes to select
   '''
   true = len(np.where(marker==1)[0])*2
   scorelist = []
   for electrode in range(n):
      correct = 0
      for j in range(1800):
         event_to_test = nosort[electrode,:,j]
         amp = np.max(event_to_test) - np.min(event_to_test)
         if ntg[electrode] < amp:
            #then classify as true, check with marker
            if j < 900:
               if marker[j] == 1:
                  correct += 1
            else:
               index = j - 900
               if marker[index] == 1:
                  correct += 1
      score = correct/true
      if score < 1:
         scorelist.append(score)
      else:
         scorelist.append(0)

   score_array = np.array(scorelist)
   sorted_indices = np.argsort(score_array)[::-1]
   top_n_indices = sorted_indices[:e]
   return top_n_indices

   

#[31, 32, 12, 13, 19, 16, 11, 14, 18, 20]
#selection = [30, 31, 11, 12, 18, 15, 10, 13, 17, 19, 0, 29, 1, 28, 14, 16]
selection = np.linspace(0, 31, 32, dtype=int)
ImprovedSelection = [10, 2, 17, 21, 22, 25, 23, 24, 30, 6, 9, 4, 19, 20, 27]
n = len(selection)


nontargetuse, targetuse, nosortuse, marker = sf.ReadFile("TMA4851_EIT\SignalProcessing\P300\s53.mat", 0, 600, selection)
ntp = MakePeak(nontargetuse)

def SelectSignal(nontarget, target, n, permute):
   '''
   n signals in total, where only one is target signal
   Turn on (1) and off (0) permute to shuffle the signals
   '''

   targetSignal = target[:,:,299]
   nontargetSignal = nontarget[:,102:,1:n]
   # Stack the signals along the third dimension
   stackedSignal = np.dstack((targetSignal, nontargetSignal))

   # Generate a random permutation of the third axis
   if permute == 1:
      perm = np.random.permutation(stackedSignal.shape[2])
   # Apply the permutation to the third axis
      stackedSignal = stackedSignal[:,:,perm]

   return stackedSignal

def evaluate_Y(n):
   '''
   n signals in total, where only one is target signal
   '''
   selection = np.linspace(0, 31, 32, dtype=int)
   nontargetuse, targetuse, nosortuse, marker = sf.ReadFile("TMA4851_EIT\SignalProcessing\P300\s53.mat", 0, 600, selection)
   SS = SelectSignal(nontargetuse, targetuse, n, 1)
   
   #One run for Col index
   for j in range(n):
      if ClassificationWithPeak(ntp, SS, 0.7446, 32, j):
         indexCol = j

   #Regenerate mock signal for row index
   SS = SelectSignal(nontargetuse, targetuse, n, 1)
   for j in range(n):
      if ClassificationWithPeak(ntp, SS, 0.7446, 32, j):
         indexRow = j

   return [indexRow, indexCol]
#print("Performance checked list", PerformaceElectrode(ntp, nosortuse, marker, 15))

#print(get_Y(6))

#print(CheckClassPercentage(ntp, nosortuse, 0.8446, n, marker))
#print("Optimal threshold", OptimizeThresholdSimpel(ntp, targetuse, n))
# % = 0.8776 for s53, 0.8446 for s01
#Note: when increase range to 0,600, true = 0, not possible to optimize, bad success percentage


def Test():
   nontargetuse, _, nosortuse, tgtpercentage = sf.ReadFileTest("data/s01.mat", 32, 220, 500)
   ntp = MakePeak(nontargetuse)
   print("target percentage", tgtpercentage)
   print(ClassificationWithPeak(ntp, nosortuse, 0.877, 32, 1))   #This is only one classification
   print("percentage correct classification", CheckClassPercentage(ntp, nosortuse, 0.752, 32))
#Test()