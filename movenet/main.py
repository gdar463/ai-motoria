import argparse
import os
import sys

from video import determine_crop_region, init_crop_region, run_inference, save_video

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"

from debug import DebugLevel, Timing, trace

import importlib.util

import numpy as np
if importlib.util.find_spec("tensorflow") is None:
  sys.exit("TensorFlow is not installed. Please install it and try again.\n"
         "Check the TF wiki for information (https://www.tensorflow.org/install/pip)")

with Timing("TF Load") as t:
  # noinspection PyUnresolvedReferences
  from tensorflow import io as tf_io, expand_dims as tf_expand_dims, image as tf_image

import cache
from model import input_size, movenet
from image import draw_prediction, ready_image, show_image, write_image

def run_model_and_prediction_photo( path, output_path= "" ):
  # Load File
  image = tf_io.read_file(path)
  image = tf_io.decode_jpeg(image)

  # Check cache
  (in_cache, img_cache) = cache.is_in_cache(image)
  if in_cache:
    # If in cache, load cached version
    trace("cache hit")
    keypoints = np.load(img_cache)
  else:
    # If not, prepare image
    trace("cache miss")
    input_image = tf_expand_dims(image, axis=0)
    input_image = tf_image.resize_with_pad(input_image, input_size, input_size)

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

def run_model_and_prediction_video( path, output_path= "" ):
  # Load File
  video = tf_io.read_file(path)
  video = tf_io.decode_gif(video)

  num_frames, height, width, _ = video.shape
  crop_region = init_crop_region(height, width)

  output = []
  for i in range(num_frames):
    keypoints = run_inference(
      video[i, :, :, :],crop_region, crop_size=[input_size, input_size]
    )
    output.append(draw_prediction(video[i, :, :, :].numpy().astype(np.int32), keypoints, output_image_height=300))
    crop_region = determine_crop_region(keypoints, height, width)

  output = np.stack(output, axis=0)
  save_video(output, output_path)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("image")
  parser.add_argument("--video", "-v", action="store_true", required=False)
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
  if args.video:
    run_model_and_prediction_video(path, output_path)
  else:
    run_model_and_prediction_photo(path, output_path)
