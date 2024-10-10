from PIL import Image
import streamlit as st
import cv_functions.img_background as bkg_func
import tempfile
import cv2

# Page configuration
st.set_page_config(
    page_title="Vision Toolkit - Background Extractor",
    layout="wide",
    page_icon="🖼️"
)

# Page title
st.title("Background Extractor")

if __name__ == "__main__":

    opt1, opt2 = st.columns([1, 1])
    col1, col2 = st.columns([1, 1])

    if 'video_option' not in st.session_state:
        st.session_state['video_option'] = "Default Video"

    if 'bkg' not in st.session_state:
        st.session_state['bkg'] = None

    if 'byte_data' not in st.session_state:
        st.session_state['byte_data'] = None

    with opt1:

        video_path = None

        # Provide the user with options
        option = st.radio("Choose an option:",
                          ("Default Video", "Upload a video file"))

        if option != st.session_state['video_option']:
            st.session_state['video_option'] = option
            st.session_state['bkg'] = None
            st.session_state['byte_data'] = None

        if option == "Default Video":
            video_path = 'img/video_converted.mp4'

        elif option == "Upload a video file":
            st.warning(
                "1. Note: The video should be in MP4 format and have a static background (See default video as example). \n 2. Note: 5 seconds video should be sufficient \n 3. Note: High Resolution Video may not work due to limits")

            uploaded_file = st.file_uploader(
                "Upload a video file", type=["mp4"])
            if uploaded_file is not None:
                # Save the uploaded file temporarily
                temp_file = tempfile.NamedTemporaryFile(
                    delete=False, suffix=".avc1")
                temp_file.write(uploaded_file.read())
                video_path = temp_file.name

        with col1:
            if video_path is not None:
                st.video(video_path)

    placeholder = col2.empty()

    # Ensure the background image is still displayed after the download button is clicked
    if st.session_state['bkg'] is not None:
        placeholder.image(
            st.session_state['bkg'], caption='Background', use_column_width=True)

    with opt2:
        btn1, btn2 = st.columns([1, 1])
        background = None
        if video_path is not None:
            with btn1:
                if st.button("Extract Background"):
                    with placeholder:
                        st.info("⏳Extracting Background...")
                    video_seq = cv2.VideoCapture(video_path)
                    all_frames = bkg_func.icv_video_to_frames(video_seq)
                    background = bkg_func.icv_get_background(all_frames)
                    st.session_state['bkg'] = background
                    background_uint8 = cv2.convertScaleAbs(background)
                    color_bkg = cv2.cvtColor(
                        background_uint8, cv2.COLOR_RGB2BGR)
                    # Encode the image to PNG format
                    is_success, buffer = cv2.imencode(".png", color_bkg)
                    if is_success:
                        # Convert the encoded image to bytes
                        byte_data = buffer.tobytes()
                        st.session_state['byte_data'] = byte_data

            with col2:
                if st.session_state['bkg'] is not None:
                    placeholder.image(st.session_state['bkg'], caption='Background',
                                      use_column_width=True)

                    with btn2:
                        if st.session_state['bkg'] is not None:
                            # Create the download button using the byte data
                            st.download_button(
                                label="Download Background",
                                data=st.session_state['byte_data'],
                                file_name="extracted_background.png",
                                mime="image/png",
                                type='primary'
                            )
