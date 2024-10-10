# :eyes: [Vision-Toolkit](https://vision-toolkit.streamlit.app/)

## :loudspeaker: Disclaimer

This repository contains code that forms part of the deliverables for my MSc AI degreee. Unauthorized reproduction of this project, including for plagiarism or any form of academic dishonesty, is strictly prohibited. The content is intended to showcase my skills and may be used for reference purposes only with proper attribution.

## :scroll: Description

This project involves the implementation of 5 tools used for basic computer vision tasks. Most implementations are made from scratch as per requirements of the MSc module.

### 1. Image Rotation

This tool allows the user to input a degree of rotation and rotate an image. The implementation is from scratch where the image is rotated without built-in libraries.

### 2. Convolution and Filters

This tool allows a user to experiment with 3 main filters. The Gaussian Blur filter is used to apply a blur effect on an image, the Laplacian filter is used to sharpen an image and the Edge Detection filter is a combination of Gaussian Blur and Laplacian to detect edges. All implementations including the convolution process is coded from scratch.

### 3. Color Histogram

This tool generates a color histogram of an image. Color Histograms have numerous applications such as image retrieval, object recognition, and image indexing. It is also used in video analysis to detect changes in the scene.

### 4. Similarity Descriptor

This tool uses Local Binary Patterns to create local descriptors of two images and uses cosine similarity and chi-squared distance as classifier. This is a basic classifier that differentiates between a Face or Non-face image.

### 5. Background Extractor

This tool uses frame-differencing and thresholding to extract a background a video.


## :computer: Tech

- Python
- OpenCV
- Streamlit
