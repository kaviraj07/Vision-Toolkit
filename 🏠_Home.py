import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="Vision Toolkit",
    layout="wide",
    page_icon="🤖",
)

# Display the landing page content
st.title("Welcome to the Vision Toolkit!")
st.write("~ By Kaviraj Gosaye")
"""
### :scroll: Description:

This toolkit is designed to showcase basic computer vision concepts and techniques.

### :books: Modules:
"""

st.markdown("#### 1. Image Rotation Tool")
with st.expander("Expand to Read More", expanded=True):
    st.write('''This tool allows you to rotate an image by a specified angle. Input your angle of rotation and upload your image for processing. You can choose to upload an image from your local machine or use the camera option to capture an image.
    ''')
st.markdown("#### 2. Convolution and Filters Tool")
with st.expander("Expand to Read More"):
    st.write("Lorem")
st.markdown("#### 3. Color Histogram Tool")
with st.expander("Expand to Read More"):
    st.write("Lorem")
st.markdown("#### 4. Similarity Descriptor Tool")
with st.expander("Expand to Read More"):
    st.write("Lorem")
st.markdown("#### 5. Background Extractor Tool")
with st.expander("Expand to Read More"):
    st.write("Lorem")
