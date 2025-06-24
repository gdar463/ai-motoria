from typing import Any

import kagglehub
import tensorflow as tf

from timing import Timing

input_size = 192


def movenet( image: tf.Tensor ) -> Any:
  # Download and load model from TF Hub (now kaggle hub)
  path = kagglehub.model_download("google/movenet/tensorFlow2/singlepose-lightning")
  with Timing("model load"):
    saved_model = tf.saved_model.load(path)
  model = saved_model.signatures["serving_default"]

  # Cast image to tensor
  input_image: tf.Tensor = tf.cast(image, dtype=tf.int32)
  # Run prediction
  outputs = model(input_image)
  keypoints = outputs["output_0"].numpy()
  return keypoints
