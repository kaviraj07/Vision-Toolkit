import cv2
import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image


def icv_plot_hist(image_dic):
    color_channel = ["r","g","b"]

    # Create a figure and an axis
    fig, ax = plt.subplots()

    # Plot the histogram for each color channel
    for c in range(len(color_channel)):
        channel_int = image_dic[c]
        ax.plot(range(len(channel_int)), list(channel_int.values()), c=color_channel[c])

    ax.set_title("Color Histogram")
    ax.set_xlabel("Pixel Value")
    ax.set_ylabel("Frequency")

    # Save the figure to a BytesIO buffer as a PNG image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)  # Rewind the buffer

    plt.close(fig)  # Close the figure to free up memory

    return buf

def icv_histogram(image, plot=False):
    color_channel = ["r", "g", "b"]
    dic_list = []
    bin_size = 256  # Number of bins (for 0-255 range)
    total_pixels = image.shape[0] * image.shape[1]  # Total number of pixels in the image

    # Iterate over each channel: 0 - Red, 1 - Green, 2 - Blue
    for c in range(len(color_channel)):
        # Reset dictionary for each channel to count pixel intensities
        dic = {str(i): 0 for i in range(bin_size)}
        
        # Get the values of the current channel directly
        channel_values = image[:, :, c].flatten()  # Flatten the 2D channel into a 1D array

        # Count the frequency of each intensity value
        for val in channel_values:
            dic[str(val)] += 1

        for key in dic.keys():
                dic[key] = dic[key] / total_pixels  # Divide by total number of pixels

        dic_list.append(dic)

        if plot:
            plt.plot(range(bin_size), list(dic.values()), c=color_channel[c], label=color_channel[c])

    if plot:
        plt.title("Color Histogram")
        plt.xlabel("Pixel Value")
        plt.ylabel("Frequency")
        plt.legend()
        plt.show()

    return dic_list