import numpy as np
import signal_functions as sf

def MakePeak(check):
   '''
   Takes in electrode to analyze, return (max. amplitude - min. amplitude) after averaging over all events for one electrode
   '''
   maxpeak = np.max(check[:, 200:,:], axis=1) - np.min(check[:, 0:200, :], axis=1)
   peak = np.mean(maxpeak, axis=1)

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

def CheckClassPercentage(ntp, nosort, threshold, n, marker):
   '''
   Check the percentage of correctly classified target events

   nontarget: data array for non-target events
   nosort: data array not sorted after label
   threshold: the percentage of electrodes that needs to be positive to conclude a target event
   n: number of electrodes
   '''
   correct = 0
   true = 0
   false = 0
   for i in range(1800):
      truetrue = len(np.where(marker==1)[0])*2
      truefalse = len(np.where(marker==2)[0])*2
      if ClassificationWithPeak(ntp, nosort, threshold, n, i):
         true += 1
         if i < 900:
            if marker[i] == 1:
               correct += 1
         else:
            index = i - 900
            if marker[index] == 1:
               correct += 1
      else:
         false += 1
   print('Known false', truefalse)
   print('Classified false', false)
   print("Known True", truetrue)
   print("Classified True", true)
   print("Classified True True", correct)
   return correct/true

def OptimizeThresholdSimpel(nontarget, nosort, n):
   '''
   Optimize Threshold by maximizing CheckClassPercentage

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
   Evaluate the performance of each electrode with a modified classifier that returns the classification result from each electrode.

   In the end returns a list of best performing electrodes

   e: number of electrodes to include, top e performing electrodes are returned
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

def test():
   #selection = [30, 31, 11, 12, 18, 15, 10, 13, 17, 19, 0, 29, 1, 28, 14, 16]
   selection = np.linspace(0, 31, 32, dtype=int)
   #selection = [10, 2, 17, 21, 22, 25, 23, 24, 30, 6, 9, 4, 19, 20, 27] #handpicked based on active brain regions shown in figure in report
   n = len(selection)
   nontargetuse, _, nosortuse, marker = sf.ReadFile("TMA4851_EIT\SignalProcessing\P300\s01.mat", 0, 600, selection)
   ntp = MakePeak(nontargetuse)

   # Find improved electrode selection
   #print("Performance checked list", PerformaceElectrode(ntp, nosortuse, marker, 15))
   # Returns [24 25  5 22 21  4 18 31  6  2 30  7 23 27 20]

   selection = [24, 25, 5, 22, 21, 4, 18, 31, 6, 2, 30, 7, 23, 27, 20]

   n = len(selection)
   nontargetuse, _, nosortuse, marker = sf.ReadFile("TMA4851_EIT\SignalProcessing\P300\s01.mat", 0, 600, selection)
   ntp = MakePeak(nontargetuse)

   print(CheckClassPercentage(ntp, nosortuse, 0.8049, n, marker))
   # Obtain highest accuracy: 0.169 (with threshold optimized with OptimizeThresholdSimpel)

   #print("Optimal threshold", OptimizeThresholdSimpel(ntp, nosortuse, n))
   # % = 0.8776 for s53, 0.8049 for s01

test()