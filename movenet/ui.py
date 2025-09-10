import ctypes
import platform
import sys

import qtawesome as qta
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QButtonGroup, QLabel, QLineEdit, QMainWindow, QPushButton, \
    QRadioButton, QSizePolicy, \
    QVBoxLayout, \
    QWidget

from dialog import Dialog, open_file_dialog_photo, open_file_dialog_video


class MainWindow(QMainWindow):
    def __init__( self ):
        super().__init__()
        self.setFixedSize(300, 190)

        self.setWindowTitle("Movenet")
        self.setWindowIcon(qta.icon("mdi.dumbbell", color="white"))
        widget = MainWidget(self)
        self.setCentralWidget(widget)


class MainWidget(QWidget):
    def __init__( self, parent ):
        super().__init__()
        self.setFixedSize(300, 170)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        radio_label = QLabel("<p style=\"font-size:16px\">Select Input Type</p>")
        radio_label.setTextFormat(Qt.TextFormat.RichText)

        image_radio = QRadioButton()
        image_radio.setText("Image")
        image_radio.setStyleSheet("font-size: 12px")
        image_radio.setChecked(True)
        video_radio = QRadioButton()
        video_radio.setText("Video")
        video_radio.setStyleSheet("font-size: 12px")

        radio_group = QButtonGroup()
        radio_group.addButton(image_radio)
        radio_group.addButton(video_radio)
        self.radio_group = radio_group
        radio_layout = QVBoxLayout()
        radio_layout.addWidget(radio_label)
        radio_layout.addWidget(image_radio)
        radio_layout.addWidget(video_radio)
        radio_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        run_button = QPushButton()
        run_button.setText("Run Prediction")
        run_button.setStyleSheet("font-size: 14px")
        run_button.clicked.connect(self.run_prediction)
        run_button.setDisabled(True)
        self.run_button = run_button

        output_label = QLabel("<p style=\"font-size:16px\">Output File Name</p>")
        output_label.setTextFormat(Qt.TextFormat.RichText)
        output_name = QLineEdit()
        output_name.setPlaceholderText("es. output.png")
        output_name.textChanged.connect(self.text_changed)
        self.output_name = output_name

        layout = QVBoxLayout()
        layout.addLayout(radio_layout)
        layout.addWidget(output_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.output_name, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(run_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)

    def run_prediction( self ):
        if self.radio_group.checkedButton().text() == "Image":
            open_file_dialog_photo(self, self.output_name.text())
        else:
            if not self.output_name.text().endswith(".mp4"):
                Dialog("Error", "<p style=\"font-size:13px\">Output file name not valid. Only mp4 files allowed</p>").exec()
            else:
                open_file_dialog_video(self, self.output_name.text())

    def text_changed( self ):
        if self.output_name.text() != "":
            self.run_button.setDisabled(False)
        else:
            self.run_button.setDisabled(True)


if __name__ == "__main__":
    if platform.system() == "Windows":
        myappid = u'gdar463.aimotoria.1.0'
        # noinspection PyUnresolvedReferences
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
