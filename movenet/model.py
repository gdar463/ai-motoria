import os
from typing import Any

import kagglehub
from tensorflow import Tensor as tf_Tensor, cast as tf_cast, int32 as tf_int32, saved_model as tf_saved_model

from cache import get_model
from debug import MessageLevel, Timing, logger
from spinner import Spinner

input_size = 192


def movenet( image: tf_Tensor ) -> Any:
    model = get_movenet()

    # Cast image to tensor
    input_image: tf_Tensor = tf_cast(image, dtype=tf_int32)
    # Run prediction
    logger.trace("Running Movenet ...", MessageLevel.VERBOSE)
    with Spinner():
        outputs = model(input_image)
    logger.trace("Movenet done", MessageLevel.VERBOSE)
    keypoints = outputs["output_0"].numpy()
    return keypoints


def get_movenet():
    in_cache, model_path = get_model()
    if not in_cache:
        # Download and load model from TF Hub (now kaggle hub)
        path = kagglehub.model_download("google/movenet/tensorFlow2/singlepose-lightning")
        os.replace(path, model_path)
    with Timing("model load"):
        logger.trace("Loading Movenet (might take a while) ...", MessageLevel.VERBOSE)
        with Spinner():
            saved_model = tf_saved_model.load(model_path)
        logger.trace("Movenet loaded", MessageLevel.VERBOSE)
    model = saved_model.signatures["serving_default"]
    return model
