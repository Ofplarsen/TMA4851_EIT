import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyxdf
import time
from io_utils import read_xdf
from SSVEP import io_utils
import filter
from SSVEP import testing
from SSVEP.cca import rolling_cca_classification

# Load the XDF file
''''''
channels = ['Fp1', 'Fz', 'F3', 'F7', 'F9', 'FC5', 'FC1', 'C3', 'T7', 'CP5', 'CP1', 'Pz', 'P3', 'P7'
    , 'P9', 'O1', 'Oz', 'O2', 'P10', 'P8', 'P4', 'CP2', 'CP6', 'T8', 'C4', 'Cz'
    , 'FC2', 'FC6', 'F10', 'F8', 'F4', 'Fp2','AUX_1', 'ACC_X', 'ACC_Y', 'ACC_Z']
testing.run_test(np.array([4, 5, 6, 7]), 250)

filename = "Tests/28_02/SSVEP/ses-5hz/eeg/sub-SSVEP_ses-5hz_task-Default_run-001_eeg.xdf"
x0, X = read_xdf(filename)
# 01, 02
X.columns = channels
X.loc[:, "O1"].plot()
plt.show()

X1 = filter.apply_filters(X, 50, .25, (1, 15), 3)
f_k_arr = np.array([4, 5, 6, 7])
est_freqs = testing.classify(X1, f_k_arr)

est_freqs.plot()
plt.show()



