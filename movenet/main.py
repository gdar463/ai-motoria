import argparse
import os
import sys

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"

from debug import DebugLevel, Timing, trace

import importlib.util

import numpy as np
if importlib.util.find_spec("tensorflow") is None:
  sys.exit("TensorFlow is not installed. Please install it and try again.\n"
         "Check the TF wiki for information (https://www.tensorflow.org/install/pip)")

with Timing("TF Load") as t:
  # noinspection PyUnresolvedReferences
  import tensorflow as tf

import cache
from model import input_size, movenet
from image import draw_prediction, ready_image, show_image, write_image

def run_model_and_prediction(path, output_path=""):
  # Load File
  image = tf.io.read_file(path)
  image = tf.io.decode_jpeg(image)

  # Check cache
  (in_cache, img_cache) = cache.is_in_cache(image)
  if in_cache:
    # If in cache, load cached version
    trace("cache hit")
    keypoints = np.load(img_cache)
  else:
    # If not, prepare image
    trace("cache miss")
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
  parser = argparse.ArgumentParser()
  parser.add_argument("image")
  parser.add_argument("--output", "-o", required=False)
  args = parser.parse_args()
  if args.image:
    path = args.image
  else:
    path = input("Enter file path: ")
  trace(path, DebugLevel.VERBOSE)
  if args.output:
    output_path = args.output
  else:
    output_path = input("Enter output file path: ")
  trace(output_path, DebugLevel.VERBOSE)
  run_model_and_prediction(path, output_path)
