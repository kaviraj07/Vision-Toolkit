import cv2


def convert_avi_to_mp4(input_path, output_path):
    # Open the AVI file
    cap = cv2.VideoCapture(input_path)

    # Get the width, height, and frame rate of the input video
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Define the codec and create a VideoWriter object to save the output
    # note: Streamlit does not support the 'H264' or 'mp4v' codec of OpenCV

    fourcc = cv2.VideoWriter_fourcc(*'avc1')

    # fourcc = cv2.VideoWriter_fourcc(*'H264')
    out = cv2.VideoWriter(output_path, fourcc, fps,
                          (frame_width, frame_height))

    # Read and write each frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()


# Convert the video
convert_avi_to_mp4(
    'img/DatasetB.avi', 'img/test.mp4')
