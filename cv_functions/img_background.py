import cv2
import numpy as np


def icv_video_to_frames(video_seq):

    frames = []
    while video_seq.isOpened():
        success, image = video_seq.read()
        if success:
            # Convert the frame from BGR to RGB
            rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            frames.append(rgb_frame)
        else:
            break
    frames = np.array(frames)
    video_seq.release()
    return frames


def icv_get_background(frames):
    diff = []
    # the higher threshold the less noise
    threshold = 12
    for fr in range(1, frames.shape[0]):
        d = (abs(frames[fr-1] - frames[fr]) < threshold).astype(int)
        d = d*frames[fr]
        diff.append(d)

    out = np.average(np.array(diff), axis=0).astype(float)

    # Normalize the background to the 0-255 range to ensure brightness
    background_normalized = cv2.normalize(
        out, None, 0, 255, cv2.NORM_MINMAX)

    # Convert the normalized background back to uint8
    background_uint8 = background_normalized.astype(np.uint8)
    return background_uint8
