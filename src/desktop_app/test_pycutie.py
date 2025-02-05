import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.running = False
        self.initUI()

    def initUI(self):
        #nút nhấn
        self.button = QPushButton("START / STOP", self)
        self.button.clicked.connect(self.on_click)
        
        #hiển thị trạng thái
        self.label = QLabel("", self)
        
        #hiển thị logo
        self.logo_label = QLabel(self)
        pixmap = QPixmap("logo_demo.png")
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setScaledContents(True)
        
        #bố cục
        layout = QVBoxLayout()
        layout.addWidget(self.logo_label)
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setWindowTitle("YOLO WatchDog Beta 1.0")
        self.resize(400, 200)

    def on_click(self):
        if self.running:
            self.label.setText("Stopped")
        else:
            self.label.setText("Running")
        
        self.running = not self.running

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
