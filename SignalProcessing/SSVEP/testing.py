import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from SSVEP.cca import get_Y, rolling_cca_classification
#from .. import filter
import filter
import random as rnd


def create_ref(f_k_arr, sample_rate, t_max):
    t = np.arange(0, t_max, 1/sample_rate)
    index = rnd.randint(1, len(f_k_arr)-1)
    #df = pd.DataFrame(data=arr, columns=f_k_arr, index=t)
    freq = f_k_arr[index]
    ser = pd.Series(np.sin(2*np.pi*freq*t), index=t)
    return ser, index


def create_X(
        f_k_arr: np.ndarray, sample_rate: int,
        noises: list[tuple], white_noise: tuple, n_switch_points: int
):
    t_max = 100
    t = np.arange(0, t_max, 1/sample_rate)
    ref, index = create_ref(f_k_arr, sample_rate)
    n = t_max * sample_rate
    X = pd.DataFrame(data=np.empty((n, 1)), index=t, columns=["x"])
    lwr, upr = 3, 5
    switch_points = np.random.choice(
        np.arange(lwr, upr, 1/sample_rate), int(t_max/lwr)
    ).cumsum()
    # switch_points = points in time at which focus switches from one
    # flickering frequency to another.
    switch_points = np.append(np.array([0]).astype(int), switch_points)
    switch_points = switch_points[switch_points < t_max]
    switch_points = np.append(switch_points, np.array([t_max]))
    K = len(f_k_arr)
    # state = the flickering frequency currently in focus.
    state_idx = np.random.choice(
        np.arange(1, K), len(switch_points)-1
    ).cumsum() % K
    state_ser = pd.Series(data=np.empty(len(t)), index=t)
    for i in range(0, len(switch_points)-1):
        t_1, t_2 = switch_points[i], switch_points[i+1]
        f_k = f_k_arr[state_idx[i]]
        state_ser.loc[t_1:t_2] = f_k
        X.loc[t_1:t_2, "x"] = ref.loc[t_1:t_2, f_k]
    for noise in noises:
        X.iloc[:, 0] += noise[0] * np.sin(2 * np.pi * noise[1] * t)
    X.iloc[:, 0] += np.random.normal(X.iloc[:, 0], scale=white_noise * X.iloc[:, 0].std())
    return X, state_ser


def create_X_mat(
    f_k_arr: np.ndarray, sample_rate: int,
    noise_params: tuple[tuple], white_noise_sd,
    n_channels: int, t_max: float = 2,
) -> pd.DataFrame:
    t_max = 100
    t = np.arange(0, t_max, 1/sample_rate)
    ref, index = create_ref(f_k_arr, sample_rate, t_max)
    n = t_max * sample_rate
    a = np.outer(ref, np.ones(n_channels))
    X = pd.DataFrame(data=a, index=t)
    t_mat = np.outer(t, np.ones(n_channels)).astype(float)
    for noise_param in noise_params:
        X += noise_param[0] * np.sin(float(2 * np.pi * noise_param[1]) * t_mat)
    X += np.random.normal(0, scale=white_noise_sd, size=X.shape)
    print("The index: ", index)
    return X


def classify(X, f_k_arr, win=2*500, step=250, include_w_y=False):
    Y = get_Y(f_k_arr, X.index)
    return rolling_cca_classification(X, Y, win, step, include_w_y)


def run_test(
        f_k_arr, sample_rate, noises, white_noise,
        win=2*500, step=250, include_w_y=False
):
    # 1. Create plot of filtered signal
    # 2. Create plot of estimated flickering frequency vs. actual flickering frequency
    X, actual_freqs = create_X(f_k_arr, sample_rate, noises, white_noise)
    X1 = filter.apply_filters(X, 50, .25, (1, 15), 3)
    t_min, t_max = 0, 1

    if include_w_y:
        est_freqs, w_y_df = classify(X1, f_k_arr, win, step, True)
        t = X.loc[t_min:t_max, :].index
        Y = get_Y(f_k_arr, t).loc[:, est_freqs.iloc[0]]
        w_y = w_y_df.iloc[0, :].values.reshape(-1, 1)
        X_proj = Y @ w_y
        X_proj.columns = ["Projection of filtered signal onto reference signals"]
        fig, ax = plt.subplots(3, 1)
        X_proj.plot(ax=ax[2])
        ax[2].set_xlabel("t", size=15)
        ax[2].set_ylabel("amplitude", size=15)
        ax[2].legend(loc="lower left")
    else:
        est_freqs = classify(X1, f_k_arr, win, step, False)
        fig, ax = plt.subplots(2, 1)

    X.columns = ["Raw brain signal"]
    X1.columns = ["Filtered brain signal"]
    fig.suptitle("Simulated brain signal filtering", size=25)
    X.loc[t_min:t_max, :].plot(ax=ax[0], label="Raw brain signal")
    X1.loc[t_min:t_max, :].plot(ax=ax[1], label="Filtered brain signal")
    ax[0].set_xlabel("t", size=15)
    ax[1].set_xlabel("t", size=15)
    ax[0].set_ylabel("amplitude", size=15)
    ax[1].set_ylabel("amplitude", size=15)
    ax[0].legend(loc="lower left")
    ax[1].legend(loc="lower left")
    plt.show()

    fig, ax = plt.subplots()
    ax.set_title(
        "Estimating the frequency of screen flickering from brain signal", size=25
    )
    est_freqs.plot(ax=ax, label="estimated flicker frequency (Hz)")
    actual_freqs.plot(ax=ax, label="actual flicker frequency")
    ax.legend()
    ax.set_xlabel("t", size=15)
    ax.set_ylabel("Flicker frequency (Hz)", size=15)
    #actual_state_idx.plot(ax=ax)
    plt.show()

