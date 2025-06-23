import platform
import time
from pathlib import Path
from typing import Any
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"
import tensorflow as tf
import numpy as np
import cv2
import kagglehub
import hashlib

class Timing:
  def __init__(self, message):
    self.message = message
    pass
  def __enter__(self):
    self.start = time.time()
  def __exit__(self, exc_type, exc_value, traceback):
    self.end = time.time()
    print(f"{self.message}: {self.end - self.start}")

def get_image_hash(image_tensor):
  img_bytes = tf.io.encode_jpeg(tf.cast(image_tensor, tf.uint8)).numpy()
  return hashlib.md5(img_bytes).hexdigest()

if "MOTORIA_CACHE_PATH" not in os.environ:
    cache_path = Path(os.getcwd()).joinpath("cache")
else:
    cache_path = Path(os.path.expandvars(os.path.expanduser(os.environ["AOC_CACHE_PATH"])))

from image import draw_prediction

path = kagglehub.model_download("google/movenet/tensorFlow2/singlepose-lightning")
with Timing("model load"):
  saved_model = tf.saved_model.load(path)
input_size = 192

# noinspection PyShadowingNames
def movenet(image: tf.Tensor) -> Any:
  model = saved_model.signatures["serving_default"]
  input_image: tf.Tensor = tf.cast(image, dtype=tf.int32)
  outputs = model(input_image)
  keypoints = outputs["output_0"].numpy()
  return keypoints

path = "test.jpeg"
image = tf.io.read_file(path)
image = tf.io.decode_jpeg(image)
img_hash = get_image_hash(image)

if not os.path.isdir(cache_path):
  os.makedirs(cache_path)

img_cache = cache_path.joinpath(f"{img_hash}.npy")
if not os.path.exists(img_cache):
  print("cache miss")
  input_image = tf.expand_dims(image, axis=0)
  input_image = tf.image.resize_with_pad(input_image, input_size, input_size)

  keypoints = movenet(input_image)
  np.save(img_cache, keypoints)
else:
  print("cache hit")
  keypoints = np.load(img_cache)

display = tf.expand_dims(image, axis=0)
display = tf.cast(tf.image.resize_with_pad(display,1280,1280), dtype=tf.int32)
output = draw_prediction(np.squeeze(display.numpy(), axis=0), keypoints)
display_np = np.squeeze(display.numpy(), axis=0).astype(np.uint8)

display_bgr = cv2.cvtColor(display_np, cv2.COLOR_RGB2BGR)

output = draw_prediction(display_bgr, keypoints)

cv2.imwrite("output.png", output)
if not platform.uname().release.endswith("microsoft-standard-WSL2"):
  cv2.imshow("Pose Detection", output)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
else:
  os.system("wslview output.png")