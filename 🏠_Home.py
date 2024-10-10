import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="Vision Toolkit",
    layout="wide",
    page_icon="🤖",
)

# Display the landing page content
st.title("Welcome to the Vision Toolkit!")
st.write("[By Kaviraj Gosaye](https://github.com/kaviraj07)")
"""
### :scroll: Description:

This toolkit is designed to showcase basic computer vision concepts and techniques.

### :hammer_and_wrench: Tools:
"""

st.markdown("#### 1. Image Rotation")
with st.expander("Expand to Read More"):
    st.write('''This tool allows you to rotate an image by a specified angle. Input your angle of rotation and upload your image for processing. You can choose to upload an image from your local machine or use the camera option to capture an image.
    ''')
st.markdown("#### 2. Convolution and Filters")
with st.expander("Expand to Read More"):
    st.markdown("This tool demonstrates the concept of convolution and the application of filters on an image. Choose from three different filters: Gaussian Blur, Laplacian, and Edge Detection. Gaussian Blur applies a blur effect to the image, Laplacian applies a sharpening effect, and Edge Detection applies both Gaussian Blur and Laplacian filters.")
st.markdown("#### 3. Color Histogram")
with st.expander("Expand to Read More"):
    st.write("The colour histogram represents the intensity of each colour channels in that image. It is visually useful to determine the dominant colour of the picture and how the colours are distributed. Applications of color histograms include image retrieval, object recognition, and image indexing. It is also used in video analysis to detect changes in the scene.")
st.markdown("#### 4. Similarity Descriptor")
with st.expander("Expand to Read More"):
    st.markdown(''' This tool uses Local Binary Patterns (LBP) to classify images. The LBP is a simple yet efficient texture operator that labels the pixels of an image by thresholding the neighborhood of each pixel and considers the result as a binary number. The LBP is used in various applications such as texture classification, facial recognition, and image retrieval. This tool uses the LBP to classify images as either a face or a car. The base image is a face image, and the tool compares the selected image with the base image to determine if it is a face image or not. 
                
    Cosine Similarity and Chi Square distance are used to compare the global descriptors of the images. The global descriptor is computed by dividing the image into windows and computing the LBP for each window. The LBP values are then concatenated to form a global descriptor for the image. The global descriptors of the base image and the selected image are compared to determine the similarity between the images.''')

    st.markdown(
        "However, it is worth noting that LBP has some drawbacks such as it is sensitive to noise, illumination changes and local variations.")
st.markdown("#### 5. Background Extractor")
with st.expander("Expand to Read More"):
    st.write("This tool makes use of frame differencing and thresholding to extract the background from a video.")
