import mat73
import scipy
import scipy.io as sio # cannot use for v7.3 mat file
import numpy as np
import signal_functions
import matplotlib.pyplot as plt
import pandas as pd

import signal_functions as sf

#Read .mat file
EEG = mat73.loadmat("TMA4851_EIT\SignalProcessing\P300\s01.mat")
EEG.keys()
EEG['RSVP'].keys()
EEG['test'][0].keys()
EEG['train'][0].keys()

# Parameters
baseline = [-200, 0] # in ms
frame = [220, 500] # in ms

#Test data:
#testkeys = EEG['test'][0].keys()
#print(testkeys)

# pre-processing for data (no separation to test and training)
for n_calib in range(len(EEG['train'])):
  data = np.asarray(EEG['train'][n_calib]['data'])
  srate = EEG['train'][n_calib]['srate']
  data = sf.butter_bandpass_filter(data, 0.5, 10, srate, 4)
  markers = EEG['train'][n_calib]['markers_target']

  targetID = np.where(markers==1)[0]
  nontargetID = np.where(markers==2)[0]

  tmp_targetEEG = sf.extractEpoch3D(data, targetID, srate, baseline, frame, False)
  tmp_nontargetEEG = sf.extractEpoch3D(data, nontargetID, srate, baseline, frame, False)
  if n_calib == 0:
    targetEEG = tmp_targetEEG
    nontargetEEG = tmp_nontargetEEG
  else:
    targetEEG = np.dstack((targetEEG, tmp_targetEEG))
    nontargetEEG = np.dstack((nontargetEEG, tmp_nontargetEEG))
  
print('Total shape target', targetEEG.shape)

#Slice to only work with first 8 elements of targetEEG
targetEEGuse = targetEEG[:8]
print('Sliced target shape',targetEEGuse.shape)
#print('total shape nontarget', nontargetEEG.shape)

#Extract only data for the first 8 electrodes
nontargetEEGuse = nontargetEEG[:8] 
nontargetEEGuse = np.array(nontargetEEGuse)

print('Sliced nontarget shape', nontargetEEGuse.shape)

def PlotForEachElectrode():
   fig, ax = plt.subplots(2,4)  # Change this line
   for i in range(8):
      nontarget_std = np.std(nontargetEEGuse[i, :, :], axis=1)
      avg_nontarget = np.mean(nontargetEEGuse[i, :, :], axis=1) 
      avg_target = np.mean(targetEEGuse[i, :, :], axis = 1)
      t = np.linspace(220, 450, avg_nontarget.shape[0])
      ax[i//4, i%4].plot(t, avg_nontarget, color="red", label="Non-target")  # Change this line
      ax[i//4, i%4].plot(t, avg_target, color="blue", label="Target")  # Change this line
      ax[i//4, i%4].legend()  # Change this line

   plt.suptitle('Target and Non-target average signal for the first 8 electrodes')
   plt.show()

PlotForEachElectrode()  

