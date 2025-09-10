import os
import platform

import cv2
from tensorflow import expand_dims as tf_expand_dims, cast as tf_cast, image as tf_image, int32 as tf_int32
import numpy as np
from PIL import Image

from constants import COLOR_MAP, KEYPOINT_EDGE_INDS_TO_COLOR, keypoints_threshold
from debug import trace, DebugLevel


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

  # # Crop (if asked, for video)
  # if crop_region is not None:
  #   xmin = int(max(crop_region['x_min'] * width, 0.0))
  #   ymin = int(max(crop_region['y_min'] * height, 0.0))
  #   xmax = int(min(crop_region['x_max'], 0.99) * width)
  #   ymax = int(min(crop_region['y_max'], 0.99) * height)
  #   cv2.rectangle(image, (xmin, ymin), (xmax, ymax), COLOR_MAP['b'], 1)

  # Resize (if asked)
  if output_image_height is not None:
    output_image_width = int(output_image_height * height / width)
    trace("Resizing output image to %dx%d" % (output_image_width, output_image_height), DebugLevel.VERBOSE)
    image = cv2.resize(image, (output_image_width, output_image_height), interpolation=cv2.INTER_CUBIC)

  return image

def ready_image(image):
  display = tf_expand_dims(image, axis=0)
  display = tf_cast(tf_image.resize_with_pad(display, 1280, 1280), dtype=tf_int32)
  display_np = np.squeeze(display.numpy(), axis=0).astype(np.uint8)
  return cv2.cvtColor(display_np, cv2.COLOR_RGB2BGR)

def write_image(output, output_path):
  cv2.imwrite(output_path, output)

def show_image(output):
  # Check if running in WSL
  if platform.uname().release.endswith("microsoft-standard-WSL2"):
    # If in WSL, open with wslview
    os.system("wslview output.png")
  else:
    # Leaving OpenCV implementation if ever needed
    # # If not, let OpenCV handle it
    # cv2.imshow("Pose Detection", output)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    Image.fromarray(output).show()
