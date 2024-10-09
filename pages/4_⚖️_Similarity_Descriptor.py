from PIL import Image
import streamlit as st
import cv_functions.img_descriptor as descriptor_func
import numpy as np
import math
import cv2
import io
import time

# Page configuration
st.set_page_config(
    page_title="Vision Toolkit - Descriptor",
    layout="wide",
    page_icon="⚖️"
)

# Page title
st.title("Similarity Descriptor - Local Binary Patterns (LBP)")

if __name__ == "__main__":

    # Some information about the tool
    st.subheader("Block Diagram for Classification Process:")
    st.image("img/descriptor.jpg", use_column_width=True)

    # Load the images and convert them to BGR
    base_img = cv2.imread('img/base.jpg')
    base_img = cv2.cvtColor(base_img, cv2.COLOR_RGB2BGR)

    face_img = cv2.imread('img/face.jpg')
    face_img = cv2.cvtColor(face_img, cv2.COLOR_RGB2BGR)

    car_img = cv2.imread('img/car.jpg')
    car_img = cv2.cvtColor(car_img, cv2.COLOR_RGB2BGR)

    # Creating the columns for display
    opt1, opt2 = st.columns([1, 1])

    col1, col2 = st.columns([1, 1])

    with opt1:
        st.markdown("#### Base Image for Comparison:")
        with col1:
            st.image(base_img, caption='Face Image', use_column_width=True)

    with opt2:
        selected_image_option = st.selectbox(
            "Select an image to classify:",
            ("Face", "Car")
        )

        with col2:
            if selected_image_option == "Face":
                st.image(face_img, caption="Face", use_column_width=True)
            else:
                st.image(car_img, caption="Car", use_column_width=True)

            if selected_image_option == "Face":
                selected_image = face_img
            else:
                selected_image = car_img

    if selected_image is not None:

        # Convert the images to BGR for processing
        selected_image_bgr = cv2.cvtColor(selected_image, cv2.COLOR_RGB2BGR)
        base_image_bgr = cv2.cvtColor(base_img, cv2.COLOR_RGB2BGR)

        if st.button('Classify Image'):
            comparison_result_placeholder = st.empty()

            with comparison_result_placeholder:
                st.info(f"⏳ Classifying the image... Please wait.")

                # Get the global descriptor for the base and selected images
                base_descriptor = descriptor_func.icv_global_descriptor(
                    base_image_bgr, 32)

                selected_descriptor = descriptor_func.icv_global_descriptor(
                    selected_image_bgr, 32)

                # Compare the global descriptors with the classifier
                result = descriptor_func.icv_classifier(
                    base_descriptor, selected_descriptor)

                if result:
                    st.success("Image selected is a Face image")
                else:
                    st.error("Image selected is not a Face image")
