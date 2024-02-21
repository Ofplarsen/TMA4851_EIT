import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cca import get_Y, rolling_cca_classification
from filter import apply_filters


def create_ref(f_k_arr, sample_rate):
    t = np.arange(0, 100, 1/sample_rate)
    arr = np.array([np.sin(2 * np.pi * f_k * t) for f_k in f_k_arr]).T
    df = pd.DataFrame(data=arr, columns=f_k_arr, index=t)
    return df


def create_X(f_k_arr, sample_rate, noises: list[tuple], white_noise: tuple):
    t_max = 100
    t = np.arange(0, t_max, 1/sample_rate)
    ref = create_ref(f_k_arr, sample_rate)
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


def classify(X, f_k_arr, win=2*500, step=250):
    Y = get_Y(f_k_arr, X.index)
    state_idx = rolling_cca_classification(X, Y, win, step)
    return state_idx


def run_test(f_k_arr, sample_rate, noises, white_noise, win=2*500, step=250):
    X, actual_state_idx = create_X(f_k_arr, sample_rate, noises, white_noise)
    X1 = apply_filters(X, 50, .25, (1, 15), 3)
    est_state_idx = classify(X1, f_k_arr, win, step)
    fig, ax = plt.subplots(2, 1)
    est_state_idx.plot(ax=ax[0], label="est state")
    actual_state_idx.plot(ax=ax[0], label="true state")
    X.plot(ax=ax[1])
    ax[0].legend()
    #actual_state_idx.plot(ax=ax)
    plt.show()


