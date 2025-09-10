import qtawesome as qta
from PySide6.QtCore import Qt, QObject, Signal, Slot, QThread
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFileDialog, QLabel, QVBoxLayout

from prediction import run_photo, run_video
from image import show_image
from q_spinner import QtWaitingSpinner
from video import show_video


class Worker(QObject):
    finished = Signal(object)

    def __init__( self, fn, *args ):
        super().__init__()
        self.fn = fn
        self.args = args

    def run( self ):
        result = self.fn(*self.args)
        self.finished.emit(result)

def open_file_dialog_photo( parent, output_path ):
    filename = QFileDialog.getOpenFileName(parent, "Open File", "",
                                           "Images (*.jpg *.jpeg *.png *.bmp)", )
    if filename[0] != "":
        thread = QThread(parent)
        worker = Worker(run_photo, filename[0], output_path)
        worker.moveToThread(thread)

        output = None

        class Receiver(QObject):
            @Slot(object)
            def on_finished( self, result ):
                nonlocal output
                output = result
                parent.loading_dialog.accept()

        receiver = Receiver()
        worker.finished.connect(receiver.on_finished)

        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        thread.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(receiver.deleteLater)

        thread.start()
        parent.loading_dialog.exec()

        CompletedDialog().exec()
        show_image(output)
    else:
        Dialog("Error", "<p style=\"font-size:13px\">No file selected</p>").exec()

def open_file_dialog_video( parent, output_path ):
    filename = QFileDialog.getOpenFileName(parent, "Open File", "",
                                           "Videos (*.gif)", )
    if filename[0] != "":
        thread = QThread(parent)
        worker = Worker(run_video, filename[0], output_path)
        worker.moveToThread(thread)

        output = None

        class Receiver(QObject):
            @Slot(object)
            def on_finished( self, result ):
                nonlocal output
                output = result
                parent.loading_dialog.accept()

        receiver = Receiver()
        worker.finished.connect(receiver.on_finished)

        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        thread.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(receiver.deleteLater)

        thread.start()
        parent.loading_dialog.exec()

        CompletedDialog().exec()
        show_video(output)
    else:
        Dialog("Error", "<p style=\"font-size:13px\">No file selected</p>").exec()


class Dialog(QDialog):
    def __init__( self, title: str, message: str ):
        super().__init__()

        self.setWindowTitle(title)
        self.setWindowIcon(qta.icon("mdi.dumbbell", color="white"))

        button = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button.accepted.connect(self.accept)

        label = QLabel(message)
        label.setTextFormat(Qt.TextFormat.RichText)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)


class LoadingDialog(QDialog):
    def __init__( self ):
        super().__init__()
        self.setModal(True)
        self.setWindowTitle("Loading")
        self.setWindowIcon(qta.icon("mdi.dumbbell", color="white"))
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowType.WindowSystemMenuHint, False)
        self.setFixedSize(100, 100)

        spinner = QtWaitingSpinner(self,True, True, self.windowModality(), 70.0, 70.0, 12, 10, 5, 10)
        spinner.start()

        label = QLabel("<p style=\"font-size:13px\">Loading...</p>")
        label.setTextFormat(Qt.TextFormat.RichText)

        layout = QVBoxLayout()
        layout.addWidget(spinner, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)


class CompletedDialog(QDialog):
    def __init__( self ):
        super().__init__()
        self.setWindowTitle("Success")
        self.setWindowIcon(qta.icon("mdi.dumbbell", color="white"))
        self.setFixedSize(100, 100)

        button = QDialogButtonBox(QDialogButtonBox.StandardButton.Open)
        button.accepted.connect(self.accept)

        label = QLabel("<p style=\"font-size:13px\">Prediction complete.</p>")
        label.setTextFormat(Qt.TextFormat.RichText)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)
