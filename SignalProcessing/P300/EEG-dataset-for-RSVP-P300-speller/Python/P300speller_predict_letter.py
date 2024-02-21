import mat73
import numpy as np
from functions import func_preproc as preproc

# One need to specify Data directory
#data_dir = "/Volumes/T5_2TB/Matlab_workspace/P3BCI2017_current/Won2021/Data/"
#nsub = 10
#EEG = mat73.loadmat(data_dir+'s{:02d}.mat'.format(int(nsub)))
root = "C:/Users/tbaad/Sync/Education/2024/EiT/SignalProcessing/P300/EEG-dataset-for-RSVP-P300-speller/Data"
proj_root = "C:/Users/tbaad/Sync/Education/2024/EiT/SignalProcessing"
data_root = proj_root + "/P300/EEG-dataset-for-RSVP-P300-speller/Data"
file = "s01.mat"
full_path = data_root + "/" + file
EEG = mat73.loadmat(full_path)

"""
Abbreviations:
- chanlocs = channel locations
- senloc = sensor locations
"""
#'''

# PART 1 -  Pre-processing for training EEG
# There are two calibration rounds, meaning that n_calib stops after n_calib = 1.
# pre-defined parameters
# Data dimension for
targetEEG, nontargetEEG, distance = preproc.separate_data(EEG["train"])


# training target Data
down_target = preproc.decimation_by_avg(targetEEG, 24)
down_nontarget = preproc.decimation_by_avg(nontargetEEG, 24)

ch_target, frame_target, trial_target = down_target.shape
ch_nontarget, frame_nontarget, trial_nontarget = down_nontarget.shape

# ch x time x trial -> (ch* time) x trial -> trial x (ch*time)
feat_target = np.reshape(down_target, (ch_target*frame_target, trial_target)).transpose()
feat_nontarget = np.reshape(down_nontarget, (ch_nontarget*frame_nontarget, trial_nontarget)).transpose()

# labels - (+1) for target and (-1) for nontarget
y_target = np.ones((feat_target.shape[0],1))
y_nontarget = -np.ones((feat_nontarget.shape[0],1))

print('Training target features shape', feat_target.shape)
print('Training nontarget features shape', feat_nontarget.shape)

feat_train = np.vstack((feat_target, feat_nontarget))
y_train = np.vstack((y_target, y_nontarget))

# shuffle target and nontarget indices
np.random.seed(101)
idx_train = np.arange(feat_train.shape[0])
np.random.shuffle(idx_train)
feat_train = feat_train[idx_train, :]
y_train = y_train[idx_train, :]
print('Training features shape', feat_train.shape)
print('Training labels shape', y_train.shape)

# Training
"""
# Train linear classifier and save the model - can apply own classification model
feat_column = np.array(range(feat_train.shape[1]))
feat_best_column, stats_best = classifier.stepwise_linear_model(feat_train, feat_column, y_train, 0.08)
print(feat_best_column.shape)

argsort_pval = np.argsort(stats_best.pvalues)
feat_selec_column = feat_best_column[argsort_pval[range(60)]] # will only use the best 60 features
feat_train_select = feat_train[:, feat_selec_column]

mdl_linear = LinearRegression()
mdl_linear.fit(feat_train_select, y_train)
# now mdl_linear is a model for the current subject (subject-specific)

pred_train = np.sign(mdl_linear.predict(feat_train_select))
print('Training accuracy (binary - target or nontarget): {:02f}'.format(np.sum(pred_train==y_train) / len(pred_train)))

# PART 2 - Calculate Letter detection accuracy with test EEG
# Ingredients for P300 speller
spellermatrix = ['A', 'B', 'C', 'D', 'E', 'F', 
                 'G', 'H', 'I', 'J', 'K', 'L',
                 'M', 'N', 'O', 'P', 'Q', 'R',
                 'S', 'T', 'U', 'V', 'W', 'X',
                 'Y', 'Z', '1', '2', '3', '4',
                 '5', '6', '7', '8', '9', '_']
Config_P3speller = {"seq_code": range(1,13), "full_repeat": 15, "spellermatrix": spellermatrix}
Params_P3speller = {"freq": [0.5, 10], "frame": [0, 600], "baseline": [-200, 0], "select_ch": range(1, 33)}

for n_test in range(len(EEG['test'])):
    cur_eeg = EEG['test'][n_test]
    Data = np.asarray(cur_eeg['Data'])

    srate = cur_eeg['srate']
    Data = butter_bandpass_filter(Data, 0.5, 10, srate, 4)
    markers = cur_eeg['markers_target']
    word_len = int(cur_eeg['nbTrials'] / (len(Config_P3speller['seq_code'])*Config_P3speller['full_repeat']))

    markers_seq = cur_eeg['markers_seq']
    letter_idx = np.where(np.isin(markers_seq, Config_P3speller['seq_code']))[0]

    unknownEEG = preproc.extractEpoch3D(Data, letter_idx, srate, baseline, frame, False)
    down_unknown = preproc.decimation_by_avg(unknownEEG, 24)
    ch_unknown, frame_unknown, trial_unnknown = down_unknown.shape
    feat_unknown = np.reshape(down_unknown, (ch_unknown*frame_unknown, trial_unnknown))
    feat_unknown = feat_unknown.transpose()

    # opt - calculate the all classification results from feat_unknown
    pred_unknown = mdl_linear.predict(feat_unknown[:, feat_selec_column]) # your answers // can apply own classification algorithm
    ans_letters = preproc.detect_letter_P3speller(pred_unknown, word_len, cur_eeg['text_to_spell'], letter_idx, markers_seq, Config_P3speller)
    cur_text_result = ans_letters['text_result']

    print(f"User answer: {cur_text_result} ({int(ans_letters['correct_on_repetition'][-1])}/{int(word_len)}), accuracy: {ans_letters['acc_on_repetition'][-1]}")
"""