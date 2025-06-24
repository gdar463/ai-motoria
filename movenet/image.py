import os
import platform

import cv2
import tensorflow as tf
import numpy as np

from constants import COLOR_MAP, KEYPOINT_EDGE_INDS_TO_COLOR, keypoints_threshold


# noinspection PyUnresolvedReferences,PyUnboundLocalVariable
def draw_prediction(image, keypoints, crop_region=None, output_image_height=None):
  height, width = image.shape[:2]

  # Draw model output
  num_instances, _, _, _ = keypoints.shape
  for i in range(num_instances):
    kpts_x = keypoints[0, i, :, 1] * width
    kpts_y = keypoints[0, i, :, 0] * height
    kpts_scores = keypoints[0, i, :, 2]

    # Draw edges
    for (p1, p2), color_key in KEYPOINT_EDGE_INDS_TO_COLOR.items():
      if kpts_scores[p1] > keypoints_threshold and kpts_scores[p2] > keypoints_threshold:
        pt1 = (int(kpts_x[p1]), int(kpts_y[p1]))
        pt2 = (int(kpts_x[p2]), int(kpts_y[p2]))
        cv2.line(image, pt1, pt2, COLOR_MAP[color_key], 3)

    # Draw keypoints (joints)
    for x, y, score in zip(kpts_x, kpts_y, kpts_scores):
      if score > keypoints_threshold:
        cv2.circle(image, (int(x), int(y)), 6, COLOR_MAP['red'], -1)

  # Crop (if asked, for video)
  if crop_region is not None:
    xmin = int(max(crop_region['x_min'] * width, 0.0))
    ymin = int(max(crop_region['y_min'] * height, 0.0))
    xmax = int(min(crop_region['x_max'], 0.99) * width)
    ymax = int(min(crop_region['y_max'], 0.99) * height)
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), COLOR_MAP['b'], 1)

  # Resize (if asked)
  if output_image_height is not None:
    output_image_width = int(output_image_height * width / height)
    image = cv2.resize(image, (output_image_width, output_image_height), interpolation=cv2.INTER_CUBIC)

  return image

def ready_image(image):
  display = tf.expand_dims(image, axis=0)
  display = tf.cast(tf.image.resize_with_pad(display, 1280, 1280), dtype=tf.int32)
  display_np = np.squeeze(display.numpy(), axis=0).astype(np.uint8)
  return cv2.cvtColor(display_np, cv2.COLOR_RGB2BGR)

def show_image(output):
  cv2.imwrite("output.png", output)
  if not platform.uname().release.endswith("microsoft-standard-WSL2"):
    cv2.imshow("Pose Detection", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
  else:
    os.system("wslview output.png")