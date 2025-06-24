import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget


class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Movenet Runner")
    widget = MainWidget(self)
    self.setCentralWidget(widget)

class MainWidget(QWidget):
  def __init__(self, parent):
    super().__init__()

    run_button = QPushButton()
    run_button.setText("Run Prediction")
    run_button.setStyleSheet("font-size: 14px")
    run_button.clicked.connect(self.run_prediction)

  def run_prediction(self):
    open_file_dialog(self)

app = QApplication(sys.argv)
window = MainWindow()
window.resize(800, 600)
window.show()
sys.exit(app.exec())