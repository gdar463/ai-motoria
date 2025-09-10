from debug import MessageLevel, Timing, logger
from spinner import Spinner

with Timing("TF Load: prediction.py") as t:
    logger.trace("Loading TensorFlow (might take a while) ...", MessageLevel.VERBOSE)
    with Spinner():
        from tensorflow import io as tf_io, expand_dims as tf_expand_dims, image as tf_image
    logger.trace("TensorFlow loaded", MessageLevel.VERBOSE)
import numpy as np

import cache
from model import get_movenet, input_size, movenet
from image import draw_prediction, ready_image, show_image, write_image
from video import determine_crop_region, init_crop_region, run_inference, save_video, show_video


def run_photo( path, output_path ):
    # Load File
    image = tf_io.read_file(path)
    image = tf_io.decode_image(image)

    # Check cache
    (in_cache, img_cache) = cache.is_in_cache(image)
    if in_cache:
        # If in cache, load cached version
        logger.trace("cache hit")
        keypoints = np.load(img_cache)
    else:
        # If not, prepare image
        logger.trace("cache miss")
        input_image = tf_expand_dims(image, axis=0)
        input_image = tf_image.resize_with_pad(input_image, input_size, input_size)

        # Run prediction
        keypoints = movenet(input_image)
        # Save in cache
        np.save(img_cache, keypoints)

    # Prepare display for output
    display = ready_image(image)
    # Overlay keypoints with image
    logger.trace("Drawing keypoints on topo of image ...", MessageLevel.VERBOSE)
    with Spinner():
        output = draw_prediction(display, keypoints)
    logger.trace("Keypoints drawn", MessageLevel.VERBOSE)

    write_image(output, output_path)
    # Open image
    show_image(output)


def run_video( path, output_path, fps = 5 ):
    video = tf_io.read_file(path)
    video = tf_io.decode_gif(video)

    num_frames, height, width, _ = video.shape
    crop_region = init_crop_region(height, width)

    movenet_video = get_movenet()

    logger.trace("Running inference on video ...", MessageLevel.VERBOSE)
    with Spinner():
        output = []
        for i in range(num_frames):
            keypoints = run_inference(movenet_video,
                                      video[i, :, :, :], crop_region, crop_size=[input_size, input_size]
                                      )
            output.append(
                draw_prediction(video[i, :, :, :].numpy().astype(np.uint8), keypoints, crop_region, video=True))
            crop_region = determine_crop_region(keypoints, height, width)
    logger.trace("Inference complete", MessageLevel.VERBOSE)

    output = np.stack(output, axis=0)
    save_video(output, output_path, fps)
    show_video(output_path)
