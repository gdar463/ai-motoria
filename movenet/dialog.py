from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QLabel, QVBoxLayout

from main import run_model_and_prediction


def open_file_dialog( parent ):
  filename = QFileDialog.getOpenFileName(parent, "Apri file", "", "All Files (*)", )
  if filename[0] != "":
    run_model_and_prediction(filename[0])
  else:
    _ = Dialog("Messaggio", "<p style=\"font-size:13px\">Non hai selezionato alcun file</p>").exec()

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