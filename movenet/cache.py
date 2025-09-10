import hashlib
import os
from pathlib import Path

from tensorflow import cast as tf_cast, uint8 as tf_uint8, io as tf_io


def get_image_hash( image_tensor ):
  img_bytes = tf_io.encode_jpeg(tf_cast(image_tensor, tf_uint8)).numpy()
  return hashlib.md5(img_bytes).hexdigest()


def get_cache_path():
  if "MOTORIA_CACHE_PATH" not in os.environ:
    cache_path = Path(os.getcwd()).joinpath("cache")
  else:
    cache_path = Path(os.path.expandvars(os.path.expanduser(os.environ["MOTORIA_CACHE_PATH"])))
  if not os.path.isdir(cache_path):
    os.makedirs(cache_path)
  return cache_path


def is_in_cache(image):
  img_hash = get_image_hash(image)
  cache_path = get_cache_path()
  
  img_cache = cache_path.joinpath(f"{img_hash}.npy")
  if os.path.exists(img_cache):
    return True, img_cache
  return False, img_cache


def get_model():
  cache_path = get_cache_path()
  model_path = cache_path.joinpath("movenet")

  if not os.path.exists(model_path):
      return False, model_path
  return True, model_path