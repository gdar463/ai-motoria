import cv2

keypoints_threshold = 0.11

KEYPOINT_DICT = {
    'nose': 0,
    'left_eye': 1,
    'right_eye': 2,
    'left_ear': 3,
    'right_ear': 4,
    'left_shoulder': 5,
    'right_shoulder': 6,
    'left_elbow': 7,
    'right_elbow': 8,
    'left_wrist': 9,
    'right_wrist': 10,
    'left_hip': 11,
    'right_hip': 12,
    'left_knee': 13,
    'right_knee': 14,
    'left_ankle': 15,
    'right_ankle': 16
}

COLOR_MAP = {
    'm': (255, 0, 255),   # magenta
    'c': (255, 255, 0),   # cyan
    'y': (0, 255, 255),   # yellow
    'b': (255, 0, 0),     # blue
    'red': (147, 20, 255)
}

KEYPOINT_EDGE_INDS_TO_COLOR = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}


# noinspection PyUnresolvedReferences,PyUnboundLocalVariable
def draw_prediction(image, keypoints, crop_region=None, output_image_height=None):
  img = image.copy()
  height, width = img.shape[:2]

  num_instances, _, _, _ = keypoints.shape
  for i in range(num_instances):
    kpts_x = keypoints[0, i, :, 1] * width
    kpts_y = keypoints[0, i, :, 0] * height
    kpts_scores = keypoints[0, i, :, 2]

    for (p1, p2), color_key in KEYPOINT_EDGE_INDS_TO_COLOR.items():

      if kpts_scores[p1] > keypoints_threshold and kpts_scores[p2] > keypoints_threshold:
        pt1 = (int(kpts_x[p1]), int(kpts_y[p1]))
        pt2 = (int(kpts_x[p2]), int(kpts_y[p2]))
        cv2.line(img, pt1, pt2, COLOR_MAP[color_key], 3)

    for x, y, score in zip(kpts_x, kpts_y, kpts_scores):
      if score > keypoints_threshold:
        cv2.circle(img, (int(x), int(y)), 6, COLOR_MAP['red'], -1)

  if crop_region is not None:
    xmin = int(max(crop_region['x_min'] * width, 0.0))
    ymin = int(max(crop_region['y_min'] * height, 0.0))
    xmax = int(min(crop_region['x_max'], 0.99) * width)
    ymax = int(min(crop_region['y_max'], 0.99) * height)
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), COLOR_MAP['b'], 1)

  if output_image_height is not None:
    output_image_width = int(output_image_height * width / height)
    img = cv2.resize(img, (output_image_width, output_image_height), interpolation=cv2.INTER_CUBIC)

  return img