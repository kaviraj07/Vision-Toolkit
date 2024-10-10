import numpy as np
from numpy.linalg import norm


# function to convert bgr image to grayscale
def icv_bgr_to_gray(image):
    b = image[..., 0]
    g = image[..., 1]
    r = image[..., 2]
    grey = (0.2989 * r + 0.5870 * g + 0.1140 * b)//3

    return grey


def icv_lbp(image):

    # creating empty array to store lbp computed values
    lbp_image = np.zeros_like(image)

    # looping through image to calculate lbp
    # used bit shift operation - same as 2^7 but this approach is faster
    for i in range(1, image.shape[0]-1):
        for j in range(1, image.shape[1]-1):
            center = image[i, j]
            code = 0
            code |= (image[i-1, j-1] > center) << 0
            code |= (image[i-1, j] > center) << 1
            code |= (image[i-1, j+1] > center) << 2
            code |= (image[i, j+1] > center) << 3
            code |= (image[i+1, j+1] > center) << 4
            code |= (image[i+1, j] > center) << 5
            code |= (image[i+1, j-1] > center) << 6
            code |= (image[i, j-1] > center) << 7
            lbp_image[i-1, j-1] = code

    decimal = np.zeros_like(image)

    # convert all lbp binaries to decimal
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            binary = '{0:08b}'.format(int(lbp_image[i, j]))
            decimal[i, j] = int(binary[::-1], 2)

    return decimal


def icv_get_windows_sizes(image):

    shape = image.shape[0]
    sizes = []
    for i in range(1, shape + 1):
        if shape % i == 0:
            sizes.append(i)
    return sizes


def icv_get_windows_lbps(image, window_size):

    # divide the original image into window portions
    windows = []
    # converting image to grayscale
    gray_img = icv_bgr_to_gray(image)

    for i in range(0, gray_img.shape[0], window_size):
        for j in range(0, gray_img.shape[1], window_size):
            window = gray_img[i:i+window_size, j:j+window_size]
            windows.append(window)

    # compute lbp for each window portions
    lbps = []
    for window in windows:
        lbp = icv_lbp(window)
        lbps.append(lbp)

    return windows, lbps


def icv_global_descriptor(image, window_size):

    windows_image, lbps_image = icv_get_windows_lbps(image, window_size)

    lbps_list = []
    for window in range(len(windows_image)):
        decimal = lbps_image[window]
        max_val = np.max(decimal)

        # Check if max_val is zero to avoid division by zero
        if max_val != 0:
            decimal_norm = decimal / max_val * 255
        else:
            # If max_val is zero, set decimal_norm to an array of zeros with the same shape
            decimal_norm = np.zeros_like(decimal)

        hist, bins = np.histogram(decimal_norm.ravel(), bins=256, range=[
                                  0, 256], density=False)
        bin_width = bins[1] - bins[0]

        # handling zero division error
        total = np.sum(hist)

        if total == 0:
            density_wind = np.zeros_like(hist)
        else:
            density_wind = hist / (total * bin_width)

        lbps_list.append(density_wind)

    lbps_arr = np.array(lbps_list)
    global_arr = np.concatenate(lbps_arr, axis=0)
    return global_arr


def icv_cosine_similarity(label, sample):
    cos_similarity = np.dot(label, sample)/(norm(label)*norm(sample))
    return cos_similarity


def icv_chi_sq(label, sample):
    distance = 0.5 * np.sum([((a - b) ** 2) / (a + b + 1e-10)
                            for (a, b) in zip(label, sample)])
    return distance


def icv_classifier(label, sample):

    cos = icv_cosine_similarity(label, sample)
    chi = icv_chi_sq(label, sample)

    if cos >= 0.95 and chi <= 15:
        # Image is a face
        return True
    else:
        # Image is not a face
        return False
