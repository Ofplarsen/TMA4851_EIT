import statsmodels.api as sm
import numpy as np
from sklearn.linear_model import LinearRegression


def get_stats(dat, x_columns, y):
    x = dat[:, x_columns]
    results = sm.OLS(y, x).fit()
    return results


def stepwise_linear_model(dat, init_x_column, y_train, p_val):
    x_column = init_x_column
    
    while True:
        results_stats = get_stats(dat, x_column, y_train)
        if np.max(results_stats.pvalues) <= p_val:
            break
        else:
            backward_elim = np.argmax(results_stats.pvalues)
            x_column = np.delete(x_column, backward_elim)

    return x_column, results_stats

def decimation_by_avg(data, factor):
  """Function for replacing each sequence of previous factor samples with their average"""
  # for example, frame [0, 800]ms -> 17samples (Krusienski et al., 2006)
  # data.shape = [ch, time, trial]
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
        user_answer_string = user_answer.tobytes().decode('utf-8')
    
    correct_on_repetition[n_repeat] = len([i for i, j in zip(user_answer_string, label) if i == j])
    acc_on_repetition[n_repeat] = correct_on_repetition[n_repeat] / len(label)

  out = {"text_result": user_answer_string, "acc_on_repetition": acc_on_repetition, "correct_on_repetition": correct_on_repetition}
  return out