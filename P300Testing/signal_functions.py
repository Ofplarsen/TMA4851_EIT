from scipy.signal import butter, filtfilt
import numpy as np
import matplotlib.pyplot as plt
import mat73

#The first functions are taken directly from the publicly available code, the reading function is modified, plot functions are written with help from GitHub Copilot

def butter_lowpass_filter(data, lowcut, fs, order):
  nyq = fs/2
  low = lowcut/nyq
  b, a = butter(order, low, btype='low')
  y = filtfilt(b, a, data) # zero-phase filter # data: [ch x time]
  return y

def butter_highpass_filter(data, highcut, fs, order):
  nyq = fs/2
  high = highcut/nyq
  b, a = butter(order, high, btype='high')
  y = filtfilt(b, a, data) # zero-phase filter
  return y

def butter_bandpass_filter(data, lowcut, highcut, fs, order):
  nyq = fs/2
  low = lowcut/nyq
  high = highcut/nyq
  b, a = butter(order, [low, high], btype='band')
  # demean before filtering
  meandat = np.mean(data, axis=1)
  data = data - meandat[:, np.newaxis]
  y = filtfilt(b, a, data)
  return y

def extractEpoch3D(data, event, srate, baseline, frame, opt_keep_baseline):
  # extract epoch from 2D data into 3D [ch x time x trial]
  # input: event, baseline, frame
  # extract epoch = baseline[0] to frame[2]

  # for memory pre-allocation
  if opt_keep_baseline == True:
    begin_tmp = int(np.floor(baseline[0]/1000*srate))
    end_tmp = int(begin_tmp+np.floor(frame[1]-baseline[0])/1000*srate)
  else:
    begin_tmp = int(np.floor(frame[0]/1000*srate))
    end_tmp = int(begin_tmp+np.floor(frame[1]-frame[0])/1000*srate)
  
  epoch3D = np.zeros((data.shape[0], end_tmp-begin_tmp, len(event)))
  nth_event = 0

  for i in event:
    if opt_keep_baseline == True:
      begin_id = int(i + np.floor(baseline[0]/1000 * srate))
      end_id = int(begin_id + np.floor((frame[1]-baseline[0])/1000*srate))
    else:
      begin_id = int(i + np.floor(frame[0]/1000 * srate))
      end_id = int(begin_id + np.floor((frame[1]-frame[0])/1000*srate))
    
    tmp_data = data[:, begin_id:end_id]

    begin_base = int(np.floor(baseline[0]/1000 * srate))
    end_base = int(begin_base + np.floor(np.diff(baseline)/1000 * srate)-1)
    base = np.mean(tmp_data[:, begin_base:end_base], axis=1)

    rmbase_data = tmp_data - base[:, np.newaxis]
    epoch3D[:, :, nth_event] = rmbase_data
    nth_event = nth_event + 1

  return epoch3D

def plotdata(start_time, end_time, test, nontarget, n):
   fig, ax = plt.subplots(8,1)
   for i in range(n):
      #nontarget_std = np.std(nontarget[i, :, :], axis=1)
      avg_nontarget = np.mean(nontarget[i, :, :], axis=1) 
      avg_test = np.mean(test[i, :, :], axis = 1)
      t = np.linspace(start_time, end_time, avg_test.shape[0])
      ax[i].plot(t, avg_nontarget, color="red", label="Non-target")
      ax[i].plot(t, avg_test, color="blue", label="Target")
      ax[i].legend()
   plt.show()

def ReadFile(filename, read_start, read_end, selection):
   '''
   filename as string, n is number of electrodes
   read_start: start time (ms) where readings is interesting
   read_end: end time (ms)
   selection: list of electrodes selected
   '''
   #Read .mat file
   EEG = mat73.loadmat(filename)
   EEG.keys()
   EEG['RSVP'].keys()
   EEG['test'][0].keys()
   EEG['train'][0].keys()

   #Save data as lists
   baseline = [-200, 0] # in ms
   frame = [read_start, read_end] # in ms
   for n_calib in range(len(EEG['train'])):
      data = np.asarray(EEG['train'][n_calib]['data'])
      srate = EEG['train'][n_calib]['srate']
      data = butter_bandpass_filter(data, 0.5, 10, srate, 4)
      markers = EEG['train'][n_calib]['markers_target']

      targetID = np.where(markers==1)[0]
      nontargetID = np.where(markers==2)[0]
      #extraID = np.where(markers==0)[0]
      allID = np.where(markers > 0)[0]
      tmp_nosortEEG = extractEpoch3D(data, allID, srate, baseline, frame, False)
      tmp_targetEEG = extractEpoch3D(data, targetID, srate, baseline, frame, False)
      tmp_nontargetEEG = extractEpoch3D(data, nontargetID, srate, baseline, frame, True)#Keep baseline data to extract minimun before event
      if n_calib == 0:
         targetEEG = tmp_targetEEG
         nontargetEEG = tmp_nontargetEEG
         nosortEEG = tmp_nosortEEG
      else:
         targetEEG = np.dstack((targetEEG, tmp_targetEEG))
         nontargetEEG = np.dstack((nontargetEEG, tmp_nontargetEEG))   
         nosortEEG = np.dstack((nosortEEG, tmp_nosortEEG))
   #Extract only data for the first n electrodes
   nontargetEEGuse = nontargetEEG[selection] 
   targetEEGuse = targetEEG[selection]
   nosortEEGuse = nosortEEG[selection]
   # Get the markers for nosortEEG
   nosortMarkers = markers[allID]
   return nontargetEEGuse, targetEEGuse, nosortEEGuse, nosortMarkers

def ReadFileTest(filename,n, read_start, read_end):
   '''
   filename as string, n is number of electrodes
   read_start: start time (ms) where readings is interesting
   read_end: end time (ms)
   '''
   #Read .mat file
   EEG = mat73.loadmat(filename)
   baseline = [-200, 0]
   frame = [read_start, read_end]
   for n_test in range(len(EEG['test'])):
      data = np.asarray(EEG['test'][n_test]['data'])
      srate = EEG['test'][n_test]['srate']
      data = butter_bandpass_filter(data, 0.5, 10, srate, 4)
      markers = EEG['test'][n_test]['markers_target']

      targetID = np.where(markers==1)[0]
      nontargetID = np.where(markers==2)[0]
      allID = np.append(targetID, nontargetID)
      tmp_nosortEEG = extractEpoch3D(data, allID, srate, baseline, frame, False)
      tmp_targetEEG = extractEpoch3D(data, targetID, srate, baseline, frame, False)
      tmp_nontargetEEG = extractEpoch3D(data, nontargetID, srate, baseline, frame, True)#Keep baseline data to extract minimun before event
      if n_test == 0:
         targetEEG = tmp_targetEEG
         nontargetEEG = tmp_nontargetEEG
         nosortEEG = tmp_nosortEEG
      else:
         targetEEG = np.dstack((targetEEG, tmp_targetEEG))
         nontargetEEG = np.dstack((nontargetEEG, tmp_nontargetEEG))   
         nosortEEG = np.dstack((nosortEEG, tmp_nosortEEG))
   #Extract only data for the first n electrodes
   print('total shape target', targetEEG.shape)
   print('total shape nontarget', nontargetEEG.shape)
   print('marker shape', markers.shape)
   nontargetEEGuse = nontargetEEG[:n] 
   targetEEGuse = targetEEG[:n]
   nosortEEGuse = nosortEEG[:n]
   # Convert markers to a 2D array where each row corresponds to an electrode
   markers_2D = np.tile(markers, (n, 1))
   # Save marker data for each event for every electrode, first 20 events are 0, not marked
   markerUse = [markers_2D[i, 20:1820] for i in range(n)]
   #Pakking av markers: stacke events på electrode
   return nontargetEEGuse, targetEEGuse, nosortEEGuse, markerUse

def OrigReadFile(filename, read_start, read_end):
   '''
   filename as string, n is number of electrodes
   read_start: start time (ms) where readings is interesting
   read_end: end time (ms)
   Original function from open source code, used in SWLDA classifier
   '''
   #Read .mat file
   EEG = mat73.loadmat(filename)
   EEG.keys()
   EEG['RSVP'].keys()
   EEG['test'][0].keys()
   EEG['train'][0].keys()

   #Save data as lists
   baseline = [-200, 0] # in ms
   frame = [read_start, read_end] # in ms
# pre-processing for test data
   for n_test in range(len(EEG['test'])):
    data = np.asarray(EEG['test'][n_test]['data'])
    srate = EEG['test'][n_test]['srate']
    data = butter_bandpass_filter(data, 0.5, 10, srate, 4)
    markers = EEG['test'][n_test]['markers_target']
   
    targetID = np.where(markers==1)[0]
    nontargetID = np.where(markers==2)[0]
   
    tmp_targetEEG = extractEpoch3D(data, targetID, srate, baseline,  frame, False)
    tmp_nontargetEEG = extractEpoch3D(data, nontargetID, srate,  baseline, frame, False)
    if n_test == 0:
     targetEEG = tmp_targetEEG
     nontargetEEG = tmp_nontargetEEG
    else:
      targetEEG = np.dstack((targetEEG, tmp_targetEEG))
      nontargetEEG = np.dstack((nontargetEEG, tmp_nontargetEEG))   
   # Get the markers for nosortEEG
   return targetEEG, nontargetEEG