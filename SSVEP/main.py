import matplotlib.pyplot as plt
import numpy as np

import testing

f_k_arr = np.array([4, 5, 5.5, 6, 7, 7.4])  # fundamental frequencies

#'''
#X = io_utils.read_xdf("ERPSpellerDataWorking/dejittered-eeg.xdf")
#X = io_utils.read_xdf("ERPSpellerDataWorkingV2/dejittered-eeg.xdf")
#X = io_utils.read_xdf("BCISpellerV10/ERPSpellerData_A5_w/dejittered-eeg.xdf")
#X = io_utils.read_xdf("BCISpellerV9/BCISpeller_A_5_times_olav/dejittered-eeg.xdf")
#for col in X.columns:
#    X[col].plot()
#    plt.show()
#X = apply_filters(X, 50, .25, (1, 15), 3)
#for col in X.columns:
#    X[col].plot()
#    plt.show()
#t = X.index
#Y = cca.get_Y(f_k_arr, t)
#corrs = cca.rolling_cca_corrs(X, Y, 2*500, 250)
#corrs.plot()
#plt.show()

# testing
f_k_arr = np.array([4, 5, 5.5, 6, 7, 7.4])  # fundamental frequencies
testing.run_test(f_k_arr, 500, [(2, 20), (1, 50), (1.5, 35)], 2.5)

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
