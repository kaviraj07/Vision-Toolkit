from PIL import Image
import streamlit as st
import cv_functions.img_transformation as transform_func
import numpy as np
import cv2
import io

# Page configuration
st.set_page_config(
    page_title="Vision Toolkit - Rotation",
    layout="wide",
    page_icon="🔄"
)

st.title("Image Rotation")

if __name__ == "__main__":

    # Option to use camera or file upload
    st.markdown("### Choose an option to upload an image:")
    upload_option = st.radio("Select Image Source",
                             ("Upload from Device", "Use Camera"))

    # Initialize the image variable
    img = None

    # Option 1: Upload from device
    if upload_option == "Upload from Device":
        uploaded_file = st.file_uploader("Choose an image...", type=[
                                         "jpg", "jpeg", "png", "bmp", "tiff"])
        if uploaded_file is not None:
            img = cv2.imdecode(np.frombuffer(
                uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Option 2: Use camera
    elif upload_option == "Use Camera":
        uploaded_file = st.camera_input("Take a picture")
        if uploaded_file is not None:
            # Use PIL to open the camera image
            img_pil = Image.open(uploaded_file)
            img = np.array(img_pil)  # Convert to NumPy array
            # Convert from RGB to BGR for OpenCV
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Input from user for the degree of rotation
    rotation_degree = st.number_input(
        "Enter the degree of rotation:", min_value=-360, max_value=360, value=45)

    if uploaded_file is not None:
        # If a new file is uploaded, reset the rotated image
        if 'uploaded_file_name' not in st.session_state or st.session_state['uploaded_file_name'] != uploaded_file.name:
            st.session_state['rotated_image'] = None  # Clear rotated image
            # Track the current file using file name
            st.session_state['uploaded_file_name'] = uploaded_file.name

        # Convert the image to RGB format
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Create two columns for displaying original and rotated images side by side
        col1, col2 = st.columns(2)

        # Display the original image in the first column
        with col1:
            st.image(img, caption='Original Image', use_column_width=True)

        # Create a placeholder for the rotated image in the second column
        rotated_image_placeholder = col2.empty()

        # Initialize session state to keep track of the rotated image
        if 'rotated_image' not in st.session_state:
            st.session_state['rotated_image'] = None

        # Create two equal-sized columns for buttons
        button_col1, button_col2 = st.columns([1, 1])

        with button_col1:
            if st.button('Rotate Image'):
                # Display placeholder while rotating the image
                with rotated_image_placeholder:
                    st.info(f"⏳ Rotating the image... Please wait.")

                # convert degree to radians
                theta_1_rad = transform_func.icv_deg_to_radians(
                    rotation_degree)

                # Get the rotation matrix
                R = transform_func.icv_get_rot_matrix(theta_1_rad)

                # Rotate the image
                image_transformed = transform_func.icv_transformation(R, img)

                # Update the rotated image in the session state
                st.session_state['rotated_image'] = image_transformed

                # Display the rotated image in the placeholder
                rotated_image_placeholder.image(
                    st.session_state['rotated_image'], caption='Rotated Image', use_column_width=True)

        # Ensure the rotated image is still displayed after the download button is clicked
        if st.session_state['rotated_image'] is not None:
            rotated_image_placeholder.image(
                st.session_state['rotated_image'], caption='Rotated Image', use_column_width=True)

        # Download button for the rotated image
        with button_col2:
            if st.session_state['rotated_image'] is not None:
                image_transformed_pil = Image.fromarray(
                    st.session_state['rotated_image'])

                # Create an in-memory buffer
                img_byte_arr = io.BytesIO()

                # Save the image to the in-memory buffer in PNG format
                image_transformed_pil.save(img_byte_arr, format='PNG')

                # Get the byte data from the buffer
                img_byte_arr = img_byte_arr.getvalue()

                # Create the download button using the byte data
                st.download_button(
                    label="Download Rotated Image",
                    data=img_byte_arr,
                    file_name="rotated_image.png",
                    mime="image/png"
                )
