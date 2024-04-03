import mat73
import scipy
import scipy.io as sio # cannot use for v7.3 mat file
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import signal_functions as sf
import linear_classifier as lc

selection = np.linspace(0, 31, 32, dtype=int)
targetEEG, nontargetEEG = sf.OrigReadFile("EiT/data/s53.mat", 0, 600)

print(targetEEG.shape)
print(nontargetEEG.shape)

# Prepare for training
down_target = lc.decimation_by_avg(targetEEG, 24)
down_nontarget = lc.decimation_by_avg(nontargetEEG, 24)

ch_target, frame_target, trial_target = down_target.shape
ch_nontarget, frame_nontarget, tiral_nontarget = down_nontarget.shape
feat_target = np.reshape(down_target, (ch_target*frame_target, trial_target))
feat_nontarget = np.reshape(down_nontarget, (ch_nontarget*frame_nontarget, tiral_nontarget))

# feature: [n_samples, n_features]
feat_target = feat_target.transpose() 
feat_nontarget = feat_nontarget.transpose()
# y: 1 for target and -1 for nontarget
y_target = np.ones((feat_target.shape[0],1))
y_nontarget = -np.ones((feat_nontarget.shape[0],1))

feat_train = np.vstack((feat_target, feat_nontarget))
y_train = np.vstack((y_target, y_nontarget))

idx_train = np.arange(feat_train.shape[0])
np.random.shuffle(idx_train)

feat_train = feat_train[idx_train, :]
y_train = y_train[idx_train, :]


# stepwisefit in Matlab for Won2021 - penter: 0.08, <premove: 0.1>, select the best 60 features only
x_column = np.array(range(feat_train.shape[1]))
while True:
  #print(x_column.shape)
  results_stats = lc.get_stats(feat_train, x_column, y_train)
  if np.max(results_stats.pvalues) <= 0.08:
    break
  else:
    backward_elim = np.array(np.where(results_stats.pvalues == np.max(results_stats.pvalues)))
    x_column = np.delete(x_column, backward_elim)

print(x_column.shape)
print(np.max(results_stats.pvalues))

argsort_pval = np.argsort(results_stats.pvalues)
x_column = x_column[argsort_pval[range(60)]]

feat_train_select = feat_train[:, x_column]
print(feat_train_select.shape)
# Linear regression
linear_model = lc.LinearRegression()
linear_model.fit(feat_train_select, y_train)

pred_train = np.sign(linear_model.predict(feat_train_select))
np.sum(pred_train==y_train) / len(pred_train)


# Save the trained linear model and the selected x_column

mdl = {"linear": linear_model, "feat_column": x_column}
# Save
nsb = 1
fname = f's{nsb}.npy'
np.save(fname, mdl) 

# Load
read_mdl = np.load(fname,allow_pickle='TRUE').item()

# TODO: sjekke i detect_letter_P3speller, finn hvor jeg kan hente ut samme type klassifiering som peakpick

#Check result
EEG = mat73.loadmat("EiT/data/s53.mat")
read_mdl = np.load(fname,allow_pickle='TRUE').item()
baseline = [-200, 0]
frame = [0, 600]

# Ingredients for P300 speller
spellermatrix = ['A', 'B', 'C', 'D', 'E', 'F', 
                 'G', 'H', 'I', 'J', 'K', 'L',
                 'M', 'N', 'O', 'P', 'Q', 'R',
                 'S', 'T', 'U', 'V', 'W', 'X',
                 'Y', 'Z', '1', '2', '3', '4',
                 '5', '6', '7', '8', '9', '_']
Config_P3speller = {"seq_code": range(1,13), "full_repeat": 15, "spellermatrix": spellermatrix}

for n_test in range(len(EEG['test'])):
  cur_eeg = EEG['test'][n_test]
  data = np.asarray(cur_eeg['data'])
  srate = cur_eeg['srate']
  data = sf.butter_bandpass_filter(data, 0.5, 10, srate, 4)
  markers = cur_eeg['markers_target']
  word_len = int(cur_eeg['nbTrials'] / (len(Config_P3speller['seq_code'])*Config_P3speller['full_repeat']))

  markers_seq = cur_eeg['markers_seq']
  letter_idx = np.where(np.isin(markers_seq, Config_P3speller['seq_code']))[0]

  unknownEEG = sf.extractEpoch3D(data, letter_idx, srate, baseline, frame, False)
  down_unknown = lc.decimation_by_avg(unknownEEG, 24)
  ch_unknown, frame_unknown, trial_unnknown = down_unknown.shape
  feat_unknown = np.reshape(down_unknown, (ch_unknown*frame_unknown, trial_unnknown))
  feat_unknown = feat_unknown.transpose()

  # opt - calculate the all classification results from feat_unknown
  pred_unknown = read_mdl['linear'].predict(feat_unknown[:, read_mdl['feat_column']]) # your answers

  ans_letters = lc.detect_letter_P3speller(pred_unknown, word_len, cur_eeg['text_to_spell'], letter_idx, markers_seq, Config_P3speller);
  cur_text_result = ans_letters['text_result']
  print(f"User answer: {cur_text_result} ({int(ans_letters['correct_on_repetition'][-1])}/{int(word_len)}), accuracy: {ans_letters['acc_on_repetition'][-1]}")

  print(f"Accuracy one letter: {ans_letters['acc_on_repetition'][-1]**(1/word_len)}")
  