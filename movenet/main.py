import os
import sys

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"

from timing import Timing

import numpy as np
try:
  with Timing("TF Load") as t:
    import tensorflow as tf
except ImportError:
  sys.exit("TensorFlow is not installed. Please install it and try again.\n"
           "Check the TF wiki for information (https://www.tensorflow.org/install/pip)")

import cache
from model import input_size, movenet
from image import draw_prediction, ready_image, show_image, write_image

def run_model_and_prediction(path, output_path=""):
  # Load File
  image = tf.io.read_file(path)
  image = tf.io.decode_jpeg(image)

  # Check cache
  in_cache, img_cache = cache.is_in_cache(image)
  if in_cache:
    # If in cache, load cached version
    print("cache hit")
    keypoints = np.load(img_cache)
  else:
    # If not, prepare image
    print("cache miss")
    input_image = tf.expand_dims(image, axis=0)
    input_image = tf.image.resize_with_pad(input_image, input_size, input_size)

    # Run prediction
    keypoints = movenet(input_image)
    # Save in cache
    np.save(img_cache, keypoints)

  # Prepare display for output
  display = ready_image(image)
  # Overlay keypoints with image
  output = draw_prediction(display, keypoints)

  # Save image
  if output_path != "":
    write_image(output, output_path)
  # Open image
  show_image(output)

if __name__ == "__main__":
  path = input("Enter file path: ")
  output_path = input("Enter output file path: ")
  run_model_and_prediction(path, output_path)