import numpy as np


spellermatrix = np.array([
    ['A', 'B', 'C', 'D', 'E', 'F'],
    ['G', 'H', 'I', 'J', 'K', 'L'],
    ['M', 'N', 'O', 'P', 'Q', 'R'],
    ['S', 'T', 'U', 'V', 'W', 'X'],
    ['Y', 'Z', '1', '2', '3', '4'],
    ['5', '6', '7', '8', '9', '_']
]).astype(str)


def text_to_coords(text):
    coords = np.empty((len(text), 2)).astype(int)
    i = 0
    for letter in text:
        coords[i, :] = 1 + np.asarray(np.where(spellermatrix==letter))[:, 0]
        i += 1
    return coords


def shrink_3rd_dimension_x_to_y(x, y):
    shrink_factor = int(x.shape[1] / y.shape[1])
    x = np.mean(y.reshape(y.shape + (shrink_factor,)), axis=2)
    return x, y
