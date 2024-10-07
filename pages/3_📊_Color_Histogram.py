from PIL import Image
import streamlit as st
import cv_functions.img_histogram as color_hist_func
import numpy as np
import cv2
import io

# Set the page configuration
st.set_page_config(
    page_title="Vision Toolkit - Color Histogram",
    layout="wide",
    page_icon=":bar_chart:"
)

st.title("Color Histogram")


if __name__ == "__main__":

    # Initialize the image variable
    img = None
    img_bgr = None

    # Option to use camera or file upload
    st.markdown("### Choose an option to upload an image:")

    upload_option = st.radio("Select Image Source", ("Upload from Device", "Use Camera"))

    # Option 1: Upload from device
    if upload_option == "Upload from Device":
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "bmp", "tiff"])
        if uploaded_file is not None:
            img = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Option 2: Use camera
    elif upload_option == "Use Camera":
        uploaded_file = st.camera_input("Take a picture")
        if uploaded_file is not None:
            # Use PIL to open the camera image
            img_pil = Image.open(uploaded_file)
            img = np.array(img_pil)  # Convert to NumPy array
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Convert from RGB to BGR for OpenCV


    if uploaded_file is not None:
        # If a new file is uploaded, reset the histogram image
        if 'uploaded_file_name' not in st.session_state or st.session_state['uploaded_file_name'] != uploaded_file.name:
            st.session_state['histogram'] = None  # Clear Histogram image
            st.session_state['uploaded_file_name'] = uploaded_file.name  # Track the current file using file name
        
        # Convert the image to RGB format
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Create two columns for displaying original and histogram images side by side
        col1, col2 = st.columns(2)

        # Display the original image in the first column
        with col1:
            st.image(img, caption='Original Image', use_column_width=True)

        # Create a placeholder for the histogram image in the second column
        histogram_placeholder = col2.empty()

        # Initialize session state to keep track of the histogram image
        if 'histogram' not in st.session_state:
            st.session_state['histogram'] = None

        button_col1, button_col2 = st.columns([1, 1])  # Create two equal-sized columns for buttons

    
        with button_col1:
            if st.button('Create Color Histogram'):
                # Display placeholder while rotating the image
                with histogram_placeholder:
                    st.info(f"⏳ Creating the color histogram... Please wait.")

                # revert_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                hist = color_hist_func.icv_histogram(img)
                
                image_transformed = color_hist_func.icv_plot_hist(hist)
                
                # Update the Histogram image in the session state
                st.session_state['histogram'] = image_transformed

                # Display the histogram image in the placeholder
                histogram_placeholder.image(st.session_state['histogram'], caption='Histogram Image', use_column_width=True)

        # Ensure the histogram image is still displayed after the download button is clicked
        if st.session_state['histogram'] is not None:
            histogram_placeholder.image(st.session_state['histogram'], caption='Histogram Image', use_column_width=True)

        # Download button for the histogram image
        with button_col2:
            if st.session_state['histogram'] is not None:

                # Create the download button using the byte data
                st.download_button(
                    label="Download Histogram Image",
                    data= st.session_state['histogram'],
                    file_name="histogram.png",
                    mime="image/png"
                )
