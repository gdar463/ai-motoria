import qtawesome as qta
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QLabel, QVBoxLayout

from prediction import run_photo, run_video


def open_file_dialog_photo( parent, output_path ):
    filename = QFileDialog.getOpenFileName(parent, "Open File", "",
                                           "Images (*.jpg *.jpeg *.png *.bmp)", )
    if filename[0] != "":
        run_photo(filename[0], output_path)
    else:
        Dialog("Error", "<p style=\"font-size:13px\">No file selected</p>").exec()

def open_file_dialog_video( parent, output_path ):
    filename = QFileDialog.getOpenFileName(parent, "Open File", "",
                                           "Videos (*.gif)", )
    if filename[0] != "":
        run_video(filename[0], output_path)
    else:
        Dialog("Error", "<p style=\"font-size:13px\">No file selected</p>").exec()


class Dialog(QDialog):
    def __init__( self, title: str, message: str ):
        super().__init__()

        self.setWindowTitle(title)
        self.setWindowIcon(qta.icon("mdi.dumbbell", color="white"))

        button = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button.accepted.connect(self.accept)  # type: ignore[reportUnknownVariableType]

        label = QLabel(message)
        label.setTextFormat(Qt.TextFormat.RichText)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)
