import matplotlib.pyplot as plt
import numpy as np
import testing
from SignalProcessingRepo.SignalProcessing.io_utils import read_xdf


f_k_arr = np.array([4, 5, 5.5, 6, 7, 7.4])  # fundamental frequencies

#read_xdf("SSVEP/Recent/sub-P001_2hz_square_ul_ses-S001_task-Default_run-001_eeg.xdf")

# testing
f_k_arr = np.array([4, 5, 5.5, 6, 7, 7.4])  # fundamental frequencies
testing.run_test(f_k_arr, 500, [(2, 20), (1, 50), (1.5, 35)], 2.5, include_w_y=True)

fig, ax = plt.subplots(8, 2)
for i in range(0, 8):
    ax[i, 1].plot()

#df.loc[300:400, :]

'''
cca = CCA(X, f_k_arr)
print(cca.X.columns[0])
#rho = cca.cca_windowed(cca.XY, cca.X.columns[0], 0)
#print(rho)
rho = cca.cca_single(150, cca.X.columns[0], 1)
print(rho.shape)
plt.plot(rho)
plt.show()
'''
