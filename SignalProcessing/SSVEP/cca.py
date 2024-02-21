import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cross_decomposition import CCA


def get_Y(f_k_arr, t):
    n = len(t)

    lvl_1 = np.repeat(np.array(f_k_arr), 6)
    lvl_2 = np.tile(
        np.array(["sin", "sin", "sin", "cos", "cos", "cos"]),
        len(f_k_arr)
    )
    lvl_3 = np.tile(np.arange(1, 4), 2 * len(f_k_arr))
    midx = pd.MultiIndex.from_arrays(
        [lvl_1, lvl_2, lvl_3], names=("freq", "func", "harm")
    )
    Y = pd.DataFrame(
        data=np.empty((n, len(midx))), columns=midx, index=t
    )
    i = 0
    for f_k in f_k_arr:
        # create pd.DataFrame of fundamental frequencies:
        for j in range(0, 3):
            Y.iloc[:, i + j] = np.sin(2 * np.pi * (j + 1) * f_k * t)
            Y.iloc[:, i + j + 3] = np.cos(2 * np.pi * (j + 1) * f_k * t)
        i += 6
    return Y


def cca_corr(X, Y_k):
    n_comp = min([len(X.columns), len(Y_k.columns)])
    cca_obj = CCA(n_comp, scale=True, tol=1e-9, max_iter=1000)
    cca_obj.fit(X, Y_k)
    w_x = cca_obj.x_weights_[:, 0].reshape(-1, 1)
    w_y = cca_obj.y_weights_[:, 0].reshape(-1, 1)
    return (X @ w_x).corrwith(Y_k @ w_y)


def cca_corrs(X, Y):
    f_k_arr = np.unique(Y.columns.get_level_values("freq"))
    return pd.Series({freq: cca_corr(X, Y.loc[:, freq]) for freq in f_k_arr})


def rolling_cca_classification(X, Y, win, step):
    """

    :param X: pd.DataFrame
    :param Y: dict.
    :param win: int. Rolling window.
    :param step: int. Distance between subsequent window starts.
        Window must overlap, meaning that 'step' must be smaller than 'win'.
    :return:
    """
    t = X.index
    n = len(t)
    sample_freq = int(round(n / (t[-1] - t[0])))
    J = 1 + (n - win) // step
    corr_cols = np.unique(Y.columns.get_level_values("freq"))
    corr_idx = (win//2 + np.arange(0, J*step, step))/sample_freq
    corr_df = pd.DataFrame(
        data=np.empty((len(corr_idx), len(corr_cols))),
        index=corr_idx, columns=corr_cols
    )
    for j in range(0, J):
        X_j = X.iloc[j * step: j * step + win, :]
        Y_j = Y.iloc[j * step: j * step + win, :]
        corr_df.loc[(j * step + win//2)/sample_freq, :] = cca_corrs(X_j, Y_j)
    return corr_df.idxmax(axis=1)


def rolling_cca_corrs(X, Y, win, step):
    """

    :param X: pd.DataFrame
    :param Y: dict.
    :param win: int. Rolling window.
    :param step: int. Distance between subsequent window starts.
        Window must overlap, meaning that 'step' must be smaller than 'win'.
    :return:
    """
    t = X.index
    n = len(t)
    sample_freq = int(round(n / (t[-1] - t[0])))
    J = 1 + (n - win) // step
    corr_cols = np.unique(Y.columns.get_level_values("freq"))
    corr_idx = (win//2 + np.arange(0, J*step, step))/sample_freq
    corr_df = pd.DataFrame(
        data=np.empty((len(corr_idx), len(corr_cols))),
        index=corr_idx, columns=corr_cols
    )
    for j in range(0, J):
        print(j, "/", J)
        X_j = X.iloc[j * step: j * step + win, :]
        Y_j = Y.iloc[j * step: j * step + win, :]
        corr_df.loc[(j * step + win//2)/sample_freq, :] = cca_corrs(X_j, Y_j)
    return corr_df
