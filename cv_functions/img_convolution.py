import numpy as np

def icv_bgr_to_gray(image):
    b = image[...,0]
    g = image[...,1]
    r = image[...,2]
    grey = (0.2989 * r + 0.5870 * g + 0.1140 * b)//3

    return grey

def icv_kernel_norm(kernel):
    if np.sum(kernel) == 0:
        return kernel
    return kernel/np.sum(kernel)

# convolution function
def icv_convolve(image, kernel):

    kernel = icv_kernel_norm(kernel)
    
    try:
        # getting the properties of the image
        image_height, image_width, colors = image.shape
    except:
        # getting the properties of the image
        image_height, image_width = image.shape
        colors = 1
    
   
    # getting the properties of the kernel
    kernel_height, kernel_width = kernel.shape

    # padding length 
    pad_height = kernel_height // 2
    pad_width = kernel_width // 2

    # create empty image with padded zeros
    if colors == 1:
        # create empty image with padded zeros
        padded_image = np.zeros((image_height + pad_height * 2, image_width + pad_width * 2),dtype=np.uint8)
    else:
        padded_image = np.zeros((image_height + pad_height * 2, image_width + pad_width * 2, colors),dtype=np.uint8)
        
    # add the image to the new empty padded image
    padded_image[pad_height:-pad_height, pad_width:-pad_width] = image

    # create empty image to store result of convolution
    result = np.zeros_like(image,dtype=np.uint8)

    # looping through the image for convolving
    # checking if image is grayscale or colored
    # same process is applied to both but only the color channel is omitted for grayscale
    if colors == 1: 
        for c in range(colors):
            for i in range(pad_height, image_height + pad_height):
                for j in range(pad_width, image_width + pad_width):
                    # getting part of the image for convolving
                    subimage = padded_image[i - pad_height:i + pad_height + 1, j - pad_width:j + pad_width + 1]
                    # convolving with the part obtained above
                    result[i - pad_height, j - pad_width] = np.clip(np.abs(np.sum(subimage * kernel)),0,255)
    else:
        for c in range(colors):
            for i in range(pad_height, image_height + pad_height):
                for j in range(pad_width, image_width + pad_width):
                    # getting part of the image for convolving
                    subimage = padded_image[i - pad_height:i + pad_height + 1, j - pad_width:j + pad_width + 1, c]
                    # convolving with the part obtained above
                    result[i - pad_height, j - pad_width, c] = np.clip(np.abs(np.sum(subimage * kernel)),0,255)

    # normalize image pixel 0 - 255
    result = ((result - result.min()) / (result.max() - result.min()) * 255).astype(np.uint8)

    return result

gaussian_blur_kernel = np.array([[1, 2, 1], 
                     [2, 4, 2], 
                     [1, 2, 1]])

laplacian_kernel = np.array([[0, 1, 0], 
                     [1, -4, 1], 
                     [0, 1, 0]])