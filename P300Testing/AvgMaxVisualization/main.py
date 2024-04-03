import mat73
import matplotlib.pyplot as plt
import numpy as np
import preprocessing as preproc
from max_classifier import visualize_max_amp_dist



# Please change 'full_path' such that it points to the .mat file in your system:
proj_root = "C:/Users/tbaad/Sync/Education/2024/EiT/SignalProcessing"
data_root = proj_root + "/Data/P300"
file = "s01.mat"
full_path = data_root + "/" + file

EEG = mat73.loadmat(full_path)

baseline = [-200, 0]  # in ms
frame = [0, 600]  # in ms

# tgt = target, ntgt = non_target
tgt, ntgt, distance = preproc.separate_data(EEG["train"])
visualize_max_amp_dist(tgt, ntgt)
# As can be seen from the plot, the max amps are too close between target and non-target
