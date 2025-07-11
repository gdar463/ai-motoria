import hashlib
import os
from pathlib import Path

from tensorflow import cast, uint8, io


def get_image_hash( image_tensor ):
  img_bytes = io.encode_jpeg(cast(image_tensor, uint8)).numpy()
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
  