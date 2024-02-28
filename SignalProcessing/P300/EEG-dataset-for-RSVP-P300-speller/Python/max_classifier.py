import numpy as np
import matplotlib.pyplot as plt


spellermatrix = np.array([
    ['A', 'B', 'C', 'D', 'E', 'F'],
    ['G', 'H', 'I', 'J', 'K', 'L'],
    ['M', 'N', 'O', 'P', 'Q', 'R'],
    ['S', 'T', 'U', 'V', 'W', 'X'],
    ['Y', 'Z', '1', '2', '3', '4'],
    ['5', '6', '7', '8', '9', '_']
])


# amp = amplitude
# dist = distribution
def visualize_max_amp_dist(tgt, ntgt):
    """

    :param tgt: np.ndarray. Target events amp Data.
        Shape = (n_channels, timepoints, target events)
    :param ntgt: np.ndarray. Non-target events amp Data.
        Shape = (n_channels, timepoints, non-target events)
    :return: None
    """
    # Take max over time axis:
    max_tgt = np.max(tgt, axis=1)
    max_ntgt = np.max(ntgt, axis=1)

    # Take mean and std over event axis:
    mean_max_tgt = np.mean(max_tgt, axis=1)
    std_max_tgt = np.std(max_tgt, axis=1)
    mean_max_ntgt = np.mean(max_ntgt, axis=1)
    std_max_ntgt = np.std(max_ntgt, axis=1)

    n_channels = mean_max_ntgt.shape[0]

    fig, ax = plt.subplots()
    ax.plot(mean_max_tgt, color="blue", label="target max amp")
    ax.fill_between(
        x=np.arange(1, n_channels + 1),
        y1=mean_max_tgt - std_max_tgt, y2=mean_max_tgt + std_max_tgt,
        alpha=.2, color="blue",# label="target max amp"
    )
    ax.plot(mean_max_ntgt, color="red", label="non-target max amp")
    ax.fill_between(
        x=np.arange(1, n_channels + 1),
        y1=mean_max_ntgt - std_max_ntgt, y2=mean_max_ntgt + std_max_ntgt,
        alpha=.2, color="red",# label="non-target max amp"
    )
    ax.set_xlabel("channel")
    ax.set_ylabel("max amp")
    plt.legend()
    plt.show()


def train_subject(tgt, ntgt):
    """

    :param tgt: np.ndarray. Shape = (channels, time, trial)
    :param ntgt: np.ndarray. Shape = (channels, time, trial)
    :return:
    """
    max_tgt = np.max(tgt, axis=1)
    max_ntgt = np.max(ntgt, axis=1)

    # Take mean and std over event axis:
    mean_max_tgt = np.mean(max_tgt, axis=1)
    std_max_tgt = np.std(max_tgt, axis=1)
    mean_max_ntgt = np.mean(max_ntgt, axis=1)
    std_max_ntgt = np.std(max_ntgt, axis=1)

