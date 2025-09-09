from typing import Any

import kagglehub
from tensorflow import Tensor as tf_Tensor, saved_model as tf_saved_model, cast as tf_cast, int32 as tf_int32

from debug import Timing

input_size = 192


def movenet( image: tf_Tensor ) -> Any:
  # Download and load model from TF Hub (now kaggle hub)
  path = kagglehub.model_download("google/movenet/tensorFlow2/singlepose-lightning")
  with Timing("model load"):
    saved_model = tf_saved_model.load(path)
  model = saved_model.signatures["serving_default"]

  # Cast image to tensor
  input_image: tf_Tensor = tf_cast(image, dtype=tf_int32)
  # Run prediction
  outputs = model(input_image)
  keypoints = outputs["output_0"].numpy()
  return keypoints
