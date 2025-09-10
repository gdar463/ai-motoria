import argparse
import importlib.util
import sys

import filetype

from debug import LoggerClass, MessageLevel, logger
from image import show_image
from video import show_video

if importlib.util.find_spec("tensorflow") is None:
    logger.trace("TensorFlow is not installed. Please install it and try again.\n"
                 "Check the TF wiki for information (https://www.tensorflow.org/install/pip)", MessageLevel.ERROR)
    sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image")
    parser.add_argument("--video", "-v", action="store_true", required=False)
    parser.add_argument("--fps", "-f", type=int, default=5, required=False)
    parser.add_argument("-V", "--verbose", action="count", default=None)
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    logger = LoggerClass(args.verbose)

    if args.video:
        logger.trace(f'Processing video file "{args.image}"', MessageLevel.INFO)
        mime = filetype.guess_mime(args.image)
        if mime is None or mime != "image/gif":
            logger.trace("Only GIF format supported. Please convert file and try again.", MessageLevel.ERROR)
            sys.exit(1)
        from prediction import run_video

        output = run_video(args.image, args.output, args.fps)
        logger.trace("Video saved to " + args.output, MessageLevel.INFO)
        show_video(output)
    else:
        logger.trace(f'Processing image file "{args.image}"', MessageLevel.INFO)
        mime = filetype.guess_mime(args.image)
        if mime is None or (mime != "image/jpeg" and mime != "image/png" and mime != "image/bmp"):
            logger.trace("Only JPEG or PNG or BMP formats supported. Please convert file and try again.",
                         MessageLevel.ERROR)
            sys.exit(1)
        from prediction import run_photo

        output = run_photo(args.image, args.output)
        logger.trace("Image saved to " + args.output, MessageLevel.INFO)
        show_image(output)
