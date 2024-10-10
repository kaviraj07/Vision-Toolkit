import numpy as np


# function to convert deg to radians
def icv_deg_to_radians(angle):
    return np.radians(angle)


# function for bilinear interpolation
def icv_bilinear_interpolate(r, c, img):

    left_pixel = int(c)
    right_pixel = left_pixel + 1
    weight_right = right_pixel - c
    weight_left = c - left_pixel

    top_pixel = int(r)
    bottom_pixel = top_pixel + 1
    weight_top = r - top_pixel
    weight_bottom = bottom_pixel - r

    if top_pixel >= 0 and bottom_pixel < img.shape[0] and left_pixel >= 0 and right_pixel < img.shape[1]:
        inter_top = weight_left * \
            img[top_pixel, right_pixel] + \
            weight_right * img[top_pixel, left_pixel]
        inter_bottom = weight_left * \
            img[bottom_pixel, right_pixel] + \
            weight_right * img[bottom_pixel, left_pixel]
        pixel_interpolated = weight_top*inter_bottom + weight_bottom*inter_top
        return pixel_interpolated
    else:
        return 0


# function to get the boundaries of the canvas
def icv_get_boundaries(TM, row_max, col_max):
    bound = np.array(
        [[0, 0], [0, col_max-1], [row_max-1, 0], [row_max-1, col_max-1]])

    points_dash = TM.dot(bound.T)

    mins = points_dash.min(axis=1)
    maxs = points_dash.max(axis=1)

    min_row = np.int64(np.floor(mins[0]))
    min_col = np.int64(np.floor(mins[1]))

    max_row = np.int64(np.ceil(maxs[0]))
    max_col = np.int64(np.ceil(maxs[1]))

    height = max_row - min_row + 1
    width = max_col - min_col + 1

    return min_row, min_col, max_row, max_col, height, width


# the transformation function that takes as input a transformation matrix and an image
def icv_transformation(TM, img):

    min_row, min_col, max_row, max_col, height, width = icv_get_boundaries(
        TM, img.shape[0], img.shape[1])
    img_canvas = np.zeros((height, width, 3), dtype='uint8')

    # matrix_inverse = TM.T
    matrix_inverse = np.linalg.inv(TM)

    for new_i in range(min_row, max_row):
        for new_j in range(min_col, max_col):
            p_dash = np.array([new_i, new_j])
            p = matrix_inverse.dot(p_dash)
            i, j = p[0], p[1]
            if i >= 0 and i < img.shape[0] and j >= 0 and j < img.shape[1]:
                g = icv_bilinear_interpolate(i, j, img)
                img_canvas[new_i-min_row, new_j-min_col] = g
            else:
                pass
    return img_canvas


# defining rotation matrix R
def icv_get_rot_matrix(theta_1_rad):
    theta_1_rad = -theta_1_rad
    R = np.array([
        [np.cos(theta_1_rad), -np.sin(theta_1_rad)],
        [np.sin(theta_1_rad), np.cos(theta_1_rad)]
    ])
    return R


# defining the skew matrix S
def icv_get_skew_matrix(theta_2_rad):
    S = np.array([
        [1, np.tan(theta_2_rad)],
        [0, 1]
    ])
    return S
