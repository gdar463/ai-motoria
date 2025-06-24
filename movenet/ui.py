import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLineEdit, QMainWindow, QPushButton, QSizePolicy, QVBoxLayout, QWidget, \
  QLabel

from dialog import open_file_dialog


class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setFixedSize(200,100)

    self.setWindowTitle("Movenet")
    widget = MainWidget(self)
    self.setCentralWidget(widget)

class MainWidget(QWidget):
  def __init__(self, parent):
    super().__init__()
    self.setFixedSize(200,100)
    self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    output_label = QLabel("<p style=\"font-size:16px\">Output File Name</p>")
    output_label.setTextFormat(Qt.TextFormat.RichText)
    self.output_name = QLineEdit()
    self.output_name.setPlaceholderText("es. output.png")
    self.output_name.setText("output.png")

    run_button = QPushButton()
    run_button.setText("Run Prediction")
    run_button.setStyleSheet("font-size: 14px")
    run_button.clicked.connect(self.run_prediction)

    layout = QVBoxLayout()
    layout.addWidget(output_label, alignment=Qt.AlignmentFlag.AlignHCenter)
    layout.addWidget(self.output_name, alignment=Qt.AlignmentFlag.AlignHCenter)
    layout.addWidget(run_button, alignment=Qt.AlignmentFlag.AlignHCenter)
    self.setLayout(layout)

  def run_prediction(self):
    open_file_dialog(self, self.output_name.text())

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())