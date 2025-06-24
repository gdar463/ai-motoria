from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QLabel, QVBoxLayout

from main import run_model_and_prediction


def open_file_dialog( parent, output_path ):
  filename = QFileDialog.getOpenFileName(parent, "Open File", "", "Images (*.jpg *.jpeg)", )
  if filename[0] != "":
    run_model_and_prediction(filename[0], output_path)
  else:
    Dialog("Error", "<p style=\"font-size:13px\">No file selected</p>").exec()

class Dialog(QDialog):
  def __init__( self, title: str, message: str ):
    super().__init__()

    self.setWindowTitle(title)

    button = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
    button.accepted.connect(self.accept)  # type: ignore[reportUnknownVariableType]

    label = QLabel(message)
    label.setTextFormat(Qt.TextFormat.RichText)

    layout = QVBoxLayout()
    layout.addWidget(label)
    layout.addWidget(button)
    self.setLayout(layout)