# ui/widgets/region_selector.py
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QPainter, QPen


class ScreenRegionSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.start_point = None
        self.end_point = None
        self.is_selecting = False

        self.setWindowOpacity(0.3)
        self.setCursor(Qt.CrossCursor)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.showFullScreen()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.start_point = e.pos()
            self.is_selecting = True

    def mouseMoveEvent(self, e):
        if self.is_selecting:
            self.end_point = e.pos()
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.end_point = e.pos()
            self.is_selecting = False
            QTimer.singleShot(100, self.hide)

    def paintEvent(self, e):
        if self.start_point and self.end_point:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.red, 2))
            painter.drawRect(QRect(self.start_point, self.end_point))
