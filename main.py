import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('map.ui', self)
        self.spn = [0.002, 0.002]
        self.L = 'map'
        self.ll = [37.530887, 55.703118]
        self.run()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.spn = [self.spn[0] + 0.001, self.spn[1] + 0.001]
        elif event.key() == Qt.Key_PageDown:
            self.spn = [self.spn[0] - 0.001, self.spn[1] - 0.001]
        self.run()

    def run(self):
        map_params = {
            "ll": f"{self.ll[0]},{self.ll[1]}",
            "spn": f"{self.spn[0]},{str(self.spn[1])}",
            "l": self.L
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.map.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
