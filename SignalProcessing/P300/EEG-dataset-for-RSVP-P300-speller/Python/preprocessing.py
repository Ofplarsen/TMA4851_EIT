import numpy as np
#from func_filters import butter_bandpass_filter
from filters import butter_bandpass_filter
from utils import text_to_coords
from scipy.signal import butter, filtfilt, sosfiltfilt


def extractEpoch3D(data, event, srate, baseline, frame, opt_keep_baseline):
    # extract epoch from 2D Data into 3D [ch x time x trial]
    # input: event, baseline, frame
    # extract epoch = baseline[0] to frame[2]

    # for memory pre-allocation
    if opt_keep_baseline == True:
        begin_tmp = int(np.floor(baseline[0] / 1000 * srate))
        end_tmp = int(begin_tmp + np.floor(frame[1] - baseline[0]) / 1000 * srate)
    else:
        begin_tmp = int(np.floor(frame[0] / 1000 * srate))
        end_tmp = int(begin_tmp + np.floor(frame[1] - frame[0]) / 1000 * srate)

    epoch3D = np.zeros((data.shape[0], end_tmp - begin_tmp, len(event)))
    nth_event = 0
    for i in event:
        if opt_keep_baseline == True:
            begin_id = int(i + np.floor(baseline[0] / 1000 * srate))
            end_id = int(begin_id + np.floor((frame[1] - baseline[0]) / 1000 * srate))
        else:
            begin_id = int(i + np.floor(frame[0] / 1000 * srate))
            end_id = int(begin_id + np.floor((frame[1] - frame[0]) / 1000 * srate))

        tmp_data = data[:, begin_id:end_id]

        begin_base = int(np.floor(baseline[0] / 1000 * srate))
        end_base = int(begin_base + np.floor(np.diff(baseline) / 1000 * srate) - 1)
        base = np.mean(tmp_data[:, begin_base:end_base], axis=1)

        rmbase_data = tmp_data - base[:, np.newaxis]
        epoch3D[:, :, nth_event] = rmbase_data
        nth_event = nth_event + 1
    return epoch3D


def separate_data(train_data, baseline=(-200, 0), frame=(0, 600)):
    """
    For targetEEG, the size of the third dimension is given by
    trial =
    (M target letters per subject) *
    (2 target stim sequences per target letter) *
    (N repetitions of each stim sequence) *
    = 10 * 2 * 15 = 300

    The nontargetEEG of the third dimension is given by
    trial =
    (M target letters per subject) *
    (10 non_target stim sequences per target letter) *
    (N repetitions of each stim sequence) *
    = 10 * 10 * 15 = 1500

    returns targetEEG, nontargetEEG, distance
    """

    for n_calib in range(len(train_data)):
        cur_eeg = train_data[n_calib]
        data = np.asarray(cur_eeg['data'])
        srate = cur_eeg['srate']
        data = butter_bandpass_filter(data, 0.5, 10, srate, 4)
        markers = cur_eeg['markers_target']
        targetID = np.where(markers == 1)[0]
        nontargetID = np.where(markers == 2)[0]
        tmp_targetEEG = extractEpoch3D(data, targetID, srate, baseline, frame, False)
        tmp_nontargetEEG = extractEpoch3D(data, nontargetID, srate, baseline, frame, False)

        text_to_spell = cur_eeg["text_to_spell"]
        coords = text_to_coords(text_to_spell)
        target_row = np.repeat(coords[:, 0], int(len(nontargetID) / coords.shape[0]))
        target_col = np.repeat(coords[:, 1], int(len(nontargetID) / coords.shape[0]))
        # 'stim_id' is a number between 1 and 12.
        # a 'stim_id' from 1 to 6 identifies a row.
        # a 'stim_id' from 7 to 12 identifies a column.
        stim_id = cur_eeg["markers_seq"][nontargetID]
        distance_n = np.empty(len(nontargetID)).astype(int)
        distance_n[stim_id <= 6] = np.abs(stim_id - target_row)[stim_id <= 6]
        distance_n[stim_id > 6] = np.abs(stim_id - 6 - target_col)[stim_id > 6]

        if n_calib == 0:
            targetEEG = tmp_targetEEG
            nontargetEEG = tmp_nontargetEEG
            distance = distance_n
        else:
            targetEEG = np.dstack((targetEEG, tmp_targetEEG))
            nontargetEEG = np.dstack((nontargetEEG, tmp_nontargetEEG))
            distance = np.append(distance, distance_n)
    return targetEEG, nontargetEEG, distance


def decimation_by_avg(data, factor):
    """Function for replacing each sequence of previous factor samples with their average"""
    # for example, frame [0, 800]ms -> 17samples (Krusienski et al., 2006)
    # Data.shape = [ch, time, trial]
    ratio_dsample = factor
    n_ch, n_frame, n_trial = data.shape

    #print(n_frame)
    decimated_frame = int(np.floor(n_frame/ratio_dsample))
    #print(decimated_frame)

    # memory pre-allocation
    decimated_data = np.zeros((n_ch, decimated_frame, n_trial))
    #print(decimated_data.shape)

    for i in range(n_trial):
        for j in range(decimated_frame):
            cur_data = data[:, :, i]
            decimated_data[:, j, i] = np.mean(cur_data[:, j*ratio_dsample:(j+1)*ratio_dsample], axis=1)

    return decimated_data


def detect_letter_P3speller(pred_score, word_len, label, letter_ind, markers_seq, params):
    """Function for detecing letter from the predicted results from unknown EEG"""
    user_answer = np.chararray(word_len,1)
    acc_on_repetition = np.zeros(params["full_repeat"])
    correct_on_repetition = np.zeros(params["full_repeat"])
    for n_repeat in range(params["full_repeat"]):
        for n_letter in range(word_len):
            # begin and end trial for a single letter session
            begin_trial = len(params["seq_code"]) * params["full_repeat"] * (n_letter)
            end_trial = begin_trial + (n_repeat+1) * len(params["seq_code"])

            unknown_speller_code = np.zeros(len(params["seq_code"]))
            for j in range(begin_trial, end_trial):
                # predict and add lda score
                unknown_speller_code[int(markers_seq[letter_ind[j]])-1] = unknown_speller_code[int(markers_seq[letter_ind[j]])-1] + pred_score[j]

            row = np.argmax(unknown_speller_code[0:6])
            col = np.argmax(unknown_speller_code[6:12])
            user_answer[n_letter] = params['spellermatrix'][row*6+col]
        user_answer_string = user_answer.tobytes().decode()
        
        correct_on_repetition[n_repeat] = len([i for i, j in zip(user_answer_string, label) if i == j])
        acc_on_repetition[n_repeat] = correct_on_repetition[n_repeat] / len(label)

    out = {"text_result": user_answer_string, "acc_on_repetition": acc_on_repetition, "correct_on_repetition": correct_on_repetition}
    return out
