import mat73
import scipy
import scipy.io as sio # cannot use for v7.3 mat file
import numpy as np
import signal_functions
import matplotlib.pyplot as plt
import pandas as pd

import signal_functions as sf

def MakeAvgMax(check, n):
   '''
   Takes in the array to analyze, and the number of electrodes
   '''
   avgmaxlist = []
   for i in range(n):
      interest = check[i,:,:]
      avgmax = np.mean(np.max(interest, axis=1))#max over all events, then avg. of the maximass. Now has avgmax for one single elctrode
      avgmaxlist.append(avgmax)
   return np.array(avgmaxlist)

def ClassificationWithAvgMax(max_notarget, check, threshold, n):
   avgmaxcheck = MakeAvgMax(check, n)
   b = avgmaxcheck > max_notarget
   percentage = np.sum(b)/len(b)
   print("Number of events", len(b))
   print("Percentage in classification", percentage)
   if percentage >= threshold:
      return True
   else:
      return False