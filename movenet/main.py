import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"

import numpy as np
import tensorflow as tf

import cache
from model import input_size, movenet
from image import draw_prediction, ready_image, show_image, write_image

def run_model_and_prediction(path, output_path):
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
  path = input("Enter file path:")
  run_model_and_prediction(path)