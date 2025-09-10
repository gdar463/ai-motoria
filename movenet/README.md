# local movenet

Local implementation of [movenet](https://www.tensorflow.org/hub/tutorials/movenet)

## Installation

To install this project, please follow these steps:
1. Install at least [Python](https://www.python.org/) version 3.8, but not more than 3.12
2. Clone the repo 
3. Install the requirements from [pyproject.toml](pyproject.toml)
   1. Just run `pip install .` in the repo's root
4. Install Tensorflow following these [instructions](https://www.tensorflow.org/install/pip) from the TF Wiki

## Usage

If you would like to use a GUI for controlling the app, on Windows run:
```shell
py .\ui.py
```
and on Linux or macOS, run:
```shell
python3 .\ui.py
```

If you prefer to just run it from the command line, on Windows run:
```shell
py .\main.py
```
on Linux or macOS, run:
```shell
python3 .\main.py
```

## License

This project is licensed under the [GPL v3.0](../LICENSE) license

### 3rd-party libraries

This project uses the following third-party libraries:
- [Tensorflow](https://github.com/tensorflow/tensorflow), an [Apache 2.0](https://github.com/tensorflow/tensorflow/blob/master/LICENSE) licensed ML framework
- [movenet](https://www.kaggle.com/models/google/movenet), an [Apache 2.0](../LICENSE.Apache-2.0) licensed model from Google
- [OpenCV](https://github.com/opencv/opencv), an [Apache 2.0](https://github.com/opencv/opencv/blob/master/LICENSE) licensed Computer Vision library
- [KaggleHub](https://github.com/Kaggle/kagglehub), an [Apache 2.0](https://github.com/Kaggle/kagglehub/blob/master/LICENSE) licensed Python library for accessing [Kaggle](https://www.kaggle.com)
- [PySide6](https://doc.qt.io/qtforpython/), [LGPL-3.0](https://www.gnu.org/licenses/lgpl-3.0.en.html) or [GPL-3.0](../LICENSE) licensed Python bindings for the [Qt](https://www.qt.io/) framework
- [QtAwesome](https://github.com/spyder-ide/qtawesome), an [MIT](https://github.com/spyder-ide/qtawesome/blob/master/LICENSE.txt) licensed Python library for icon fonts
- [Material Design](https://github.com/Templarian/MaterialDesign), an [Apache 2.0](https://github.com/Templarian/MaterialDesign/blob/master/LICENSE) licensed Icon collection
- [Numpy](https://github.com/numpy/numpy), an [BSD](https://github.com/numpy/numpy/blob/main/LICENSE.txt) licensed Computing library
- [Pillow (PIL)](https://github.com/python-pillow/Pillow), an [MIT-CMU](https://github.com/python-pillow/Pillow/blob/main/LICENSE) licensed Imaging library
- [Colorama](https://github.com/tartley/colorama), an [BSD-3-Clause](https://github.com/tartley/colorama/blob/master/LICENSE.txt) licensed colored terminal library
- [Filetype](https://github.com/h2non/filetype.py), an [MIT](https://github.com/h2non/filetype.py/blob/master/LICENSE) licensed file type detection library