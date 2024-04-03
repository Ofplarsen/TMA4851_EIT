import numpy as np
import signal_functions as sf

def MakePeak(check):
   '''
   Takes in clipped signal for relevant electrodes, takes max amplitude - min amplitude for each event, then averages over all events for one electrode
   '''
   # Maximum amplitude
   maxpeak = np.max(check[:, 200:,:], axis=1) - np.min(check[:, 0:200, :], axis=1)

   # Average over all events, saved as a list with value for each electrode
   peak = np.mean(maxpeak, axis=1)
   
   return peak

def ClassificationWithPeak(peak_nontarget, check, threshold, n, j):
   '''
   peak_nontarget: output from MakePeak, obtained with non-target training set, a list, one peak for each electrode
   check: data array to test, not sorted after label
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
   if b > threshold:
      return True
   else:
      return False

# The following code is used to generate mock signal by retreiving from dataset, and returns coordinates evaluated with peak picking classifier

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

def evaluate_Y(m, n):
   '''
   m signals for row
   n signals (for col), where only one is target signal
   returns [row, col] coordinates of target signal evaluated with peak picking classifier
   '''

   selection = np.linspace(0, 31, 32, dtype=int)
   nontargetuse, targetuse, _, _ = sf.ReadFile("TMA4851_EIT\SignalProcessing\P300\s01.mat", 0, 600, selection)
   SS = SelectSignal(nontargetuse, targetuse, n, 1)
   ntp = MakePeak(nontargetuse)

   #One run for Col index
   for j in range(n):
      if ClassificationWithPeak(ntp, SS, 0.7446, 32, j): #Threshold specifically optimized for chosen true data
         indexCol = j

   #Regenerate mock signal for row index
   SS = SelectSignal(nontargetuse, targetuse, m, 1)
   for j in range(m):
      if ClassificationWithPeak(ntp, SS, 0.7446, 32, j):
         indexRow = j

   return [indexRow, indexCol]

#print(evaluate_Y(10, 10))