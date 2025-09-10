import os
import platform

import cv2
import numpy as np
from tensorflow import cast as tf_cast, expand_dims as tf_expand_dims, image as tf_image, int32 as tf_int32

from constants import KEYPOINT_DICT, TORSO_JOINTS, min_crop_keypoint_threshold


def init_crop_region( height, width ):
    if width > height:
        box_height = width / height
        box_width = 1
        min_y = (height - width) / 2 / height
        min_x = 0
    else:
        box_height = 1
        box_width = height / width
        min_y = 0
        min_x = (width - height) / 2 / width
    return {
        "y_min": min_y,
        "x_min": min_x,
        "y_max": min_y + box_height,
        "x_max": min_x + box_width,
        "height": box_height,
        "width": box_width,
    }


def crop_and_resize( image, crop_region, crop_size ):
    boxes = [[crop_region["y_min"], crop_region["x_min"], crop_region["y_max"], crop_region["x_max"]]]
    return tf_image.crop_and_resize(image, box_indices=[0], boxes=boxes, crop_size=crop_size)


def run_inference( movenet, image, crop_region, crop_size ):
    height, width, _ = image.shape
    input_image = crop_and_resize(tf_expand_dims(image, axis=0), crop_region, crop_size)
    input_image = tf_cast(input_image, tf_int32)
    keypoints = movenet(input=input_image)["output_0"].numpy()
    # 17 are the number of keypoints
    for i in range(17):
        keypoints[0, 0, i, 0] = (
                                    crop_region["y_min"] * height +
                                    crop_region["height"] * height * keypoints[0, 0, i, 0]
                                ) / height
        keypoints[0, 0, i, 1] = (
                                    crop_region["x_min"] * width +
                                    crop_region["width"] * width * keypoints[0, 0, i, 1]
                                ) / width
    return keypoints


def is_torso_visible( keypoints ):
    return (
        keypoints[0, 0, KEYPOINT_DICT["left_hip"], 2] > min_crop_keypoint_threshold or
        keypoints[0, 0, KEYPOINT_DICT["right_hip"], 2] > min_crop_keypoint_threshold
    ) and (
        keypoints[0, 0, KEYPOINT_DICT["left_shoulder"], 2] > min_crop_keypoint_threshold or
        keypoints[0, 0, KEYPOINT_DICT["right_shoulder"], 2] > min_crop_keypoint_threshold
    )


def determine_crop_region( keypoints, height, width ):
    if is_torso_visible(keypoints):
        target = { }
        for joint in KEYPOINT_DICT.keys():
            target[joint] = [
                keypoints[0, 0, KEYPOINT_DICT[joint], 0] * height,
                keypoints[0, 0, KEYPOINT_DICT[joint], 1] * width
            ]

        center_y = (target["left_hip"][0] + target["right_hip"][0]) / 2
        center_x = (target["left_hip"][1] + target["right_hip"][1]) / 2

        max_y_torso = 0
        max_x_torso = 0
        for joint in TORSO_JOINTS:
            dist_y = abs(center_y - target[joint][0])
            dist_x = abs(center_x - target[joint][1])
            if dist_y > max_y_torso:
                max_y_torso = dist_y
            if dist_x > max_x_torso:
                max_x_torso = dist_x

        max_y_body = 0
        max_x_body = 0
        for joint in KEYPOINT_DICT.keys():
            if keypoints[0, 0, KEYPOINT_DICT[joint], 2] < min_crop_keypoint_threshold:
                continue
            dist_y = abs(center_y - target[joint][0])
            dist_x = abs(center_x - target[joint][1])
            if dist_y > max_y_body:
                max_y_body = dist_y
            if dist_x > max_x_body:
                max_x_body = dist_x

        crop_length_half = np.amax([max_y_torso * 1.9, max_x_torso * 1.9, max_y_body * 1.2, max_x_body * 1.2])
        crop_length_half = np.amin(
            [crop_length_half, np.amax([center_x, width - center_x, center_y, height - center_y])])

        crop_corner = [center_y - crop_length_half, center_x - crop_length_half]

        if crop_length_half > max(height, width) / 2:
            return init_crop_region(height, width)
        else:
            return {
                "y_min": crop_corner[0] / height,
                "x_min": crop_corner[1] / width,
                "y_max": (crop_corner[0] + crop_length_half * 2) / height,
                "x_max": (crop_corner[1] + crop_length_half * 2) / width,
                "height": crop_length_half * 2 / height,
                "width": crop_length_half * 2 / width,
            }
    else:
        return init_crop_region(height, width)


def save_video( video, path, fps = 5 ):
    n_frames, height, width, channels = video.shape

    if channels == 3:
        colors = video[..., ::-1]
    else:
        colors = video

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output = cv2.VideoWriter(path, fourcc, fps, (width, height))

    for i in range(n_frames):
        frame = colors[i].astype(np.uint8)
        output.write(frame)

    output.release()


def show_video( path ):
    # Check if running in WSL
    if platform.uname().release.endswith("microsoft-standard-WSL2"):
        # If in WSL, open with wslview
        os.system(f"wslview {path}")
    else:
        os.startfile(path)
