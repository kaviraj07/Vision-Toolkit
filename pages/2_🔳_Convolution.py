from PIL import Image
import streamlit as st
import cv_functions.img_convolution as conv_func
import numpy as np
import cv2
import io

# Set the page configuration
st.set_page_config(
    page_title="Vision Toolkit - Convolution",
    layout="wide",
    page_icon=":white_square_button:"
)

st.title("Convolution and Kernels")


if __name__ == "__main__":

    # Initialize the image variable
    img = None

    select1, select2 = st.columns(2)

    with select1:
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

    with select2:
        # Option to select kernels
        st.markdown("### Choose a kernel to apply:")
        kernel_options = st.radio("Select Kernels", ("Gaussian Blur", "Laplacian", "Edge Detection - Gaussian Blur + Laplacian"))

    
    if uploaded_file is not None:
        # If a new file is uploaded, reset the rotated image
        if 'uploaded_file_name' not in st.session_state or st.session_state['uploaded_file_name'] != uploaded_file.name:
            st.session_state['convolved_image'] = None  # Clear convolved image
            st.session_state['uploaded_file_name'] = uploaded_file.name  # Track the current file using file name
        
        # Convert the image to RGB format
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Create two columns for displaying original and rotated images side by side
        col1, col2 = st.columns(2)

        # Display the original image in the first column
        with col1:
            st.image(img, caption='Original Image', use_column_width=True)

        # Create a placeholder for the rotated image in the second column
        convolved_image_placeholder = col2.empty()

        # Initialize session state to keep track of the rotated image
        if 'convolved_image' not in st.session_state:
            st.session_state['convolved_image'] = None

        button_col1, button_col2 = st.columns([1, 1])  # Create two equal-sized columns for buttons

        kernel_gauss = conv_func.gaussian_blur_kernel
        kernel_laplace = conv_func.laplacian_kernel

        with button_col1:
            if st.button('Apply Filter'):
                # Display placeholder while rotating the image
                with convolved_image_placeholder:
                    st.info(f"⏳ Convolving the image... Please wait.")

                if kernel_options == "Gaussian Blur":
                    gray_image = conv_func.icv_bgr_to_gray(img)
                    image_transformed = conv_func.icv_convolve(gray_image, kernel_gauss)

                elif kernel_options == "Laplacian":
                    image_transformed = conv_func.icv_convolve(img, kernel_laplace)

                elif kernel_options == "Edge Detection - Gaussian Blur + Laplacian":
                    gray_image = conv_func.icv_bgr_to_gray(img)
                    image_transformed = conv_func.icv_convolve(gray_image, kernel_gauss)
                    image_transformed = conv_func.icv_convolve(image_transformed, kernel_laplace)

                # Update the convolved image in the session state
                st.session_state['convolved_image'] = image_transformed

                # Display the rotated image in the placeholder
                convolved_image_placeholder.image(st.session_state['convolved_image'], caption='Convolved Image', use_column_width=True)

        # Ensure the rotated image is still displayed after the download button is clicked
        if st.session_state['convolved_image'] is not None:
            convolved_image_placeholder.image(st.session_state['convolved_image'], caption='Convolved Image', use_column_width=True)

        # Download button for the rotated image
        with button_col2:
            if st.session_state['convolved_image'] is not None:
                image_transformed_pil = Image.fromarray(st.session_state['convolved_image'])

                # Create an in-memory buffer
                img_byte_arr = io.BytesIO()

                # Save the image to the in-memory buffer in PNG format
                image_transformed_pil.save(img_byte_arr, format='PNG')

                # Get the byte data from the buffer
                img_byte_arr = img_byte_arr.getvalue()

                # Create the download button using the byte data
                st.download_button(
                    label="Download Convolved Image",
                    data=img_byte_arr,
                    file_name="convolved_image.png",
                    mime="image/png"
                )