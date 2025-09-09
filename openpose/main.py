import argparse
import os

import cv2
import pyopenpose as op

parser = argparse.ArgumentParser()
parser.add_argument("image")
parser.add_argument('--models-folder', '-m', default="./models", help='path to models folder')
parser.add_argument("--output", '-o', default="output.png", help='output image file name')
args = parser.parse_args()

params = dict()
params["model_folder"] = os.path.abspath(args.models_folder)
params["hand"] = False
params["face"] = False

opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

datum = op.Datum()
image = cv2.imread(os.path.abspath(args.image))
if image is None:
  raise ValueError(f"Image not found: {args.image}")
datum.cvInputData = image

vectorDatum = op.VectorDatum()
vectorDatum.append(datum)
opWrapper.emplaceAndPop(vectorDatum)

cv2.imwrite(args.output, datum.cvOutputData)
lib.show_image(datum.cvOutputData)
