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
    st.write("Lorem")
st.markdown("#### 5. Background Extractor")
with st.expander("Expand to Read More"):
    st.write("Lorem")
