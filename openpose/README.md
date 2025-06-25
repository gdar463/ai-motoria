# OpenPose Impl

Implementation of [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)

## Installation

To install this project, please follow these steps:
1. Install at least [Python](https://www.python.org/) version 3.10
2. Clone the repo 
3. Install the requirements from [pyproject.toml](pyproject.toml)
   1. Just run `pip install .` in this directory
4. Install OpenPose from its [repo](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
   1. If you want to use a Nvidia GPU with CUDA, just use the [pre-built binaries](https://github.com/CMU-Perceptual-Computing-Lab/openpose/releases)
   2. If you want to use an AMD or Intel GPU or you don't have a GPU, you'll need to [build from source](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/0_index.md) with the appropriate flags
      1. OpenPose's [license](../LICENSE.OpenPose) doesn't allow distribution of pre-built binaries, apart from CMU's provided ones
5. Install the models through the [getModels.bat](models/getModels.bat) (or on Linux/MacOS [getModels.sh](models/getModels.sh))
   1. These scripts are **NOT** licensed under GPL v3.0 (as the rest of project)
   2. These script come from the OpenPose [repo](https://github.com/CMU-Perceptual-Computing-Lab/openpose) at the following links: [Windows](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/models/getModels.bat) or [Linux/MacOS](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/models/getModels.sh) versions
   3. As such they are licensed under the OpenPose [LICENSE](../LICENSE.OpenPose)

## Usage

TODO

## License

This project is licensed under the [GPL v3.0](../LICENSE) license</br>
**EXCEPT** for [models/getModels.bat](models/getModels.bat) and the [models/getModels.sh](models/getModels.sh), as they come from [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose),
as such they're licensed under the OpenPose [LICENSE](../LICENSE.OpenPose)

### 3rd-party libraries

This project uses the following third-party libraries:
- [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose), a model from CMU, licensed under it's own [LICENSE](../LICENSE.OpenPose)
- [OpenCV](https://github.com/opencv/opencv), an [Apache 2.0](https://github.com/opencv/opencv/blob/master/LICENSE) licensed Computer Vision library
- [Numpy](https://github.com/numpy/numpy), an [BSD](https://github.com/numpy/numpy/blob/main/LICENSE.txt) licensed Computing library

[//]: # ( 
These might be use in the future, but currently no
- [PySide6]&#40;https://doc.qt.io/qtforpython/&#41;, [LGPL-3.0]&#40;https://www.gnu.org/licenses/lgpl-3.0.en.html&#41; or [GPL-3.0]&#40;../LICENSE&#41; licensed Python bindings for the [Qt]&#40;https://www.qt.io/&#41; framework
- [QtAwesome]&#40;https://github.com/spyder-ide/qtawesome&#41;, an [MIT]&#40;https://github.com/spyder-ide/qtawesome/blob/master/LICENSE.txt&#41; licensed Python library for icon fonts
- [Material Design]&#40;https://github.com/Templarian/MaterialDesign&#41;, an [Apache 2.0]&#40;https://github.com/Templarian/MaterialDesign/blob/master/LICENSE&#41; licensed Icon collection
- [Pillow &#40;PIL&#41;]&#40;https://github.com/python-pillow/Pillow&#41;, an [MIT-CMU]&#40;https://github.com/python-pillow/Pillow/blob/main/LICENSE&#41; licensed Imaging library)