from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('map.ui', self)
        self.map.setFocus()
        self.spn = [0.002, 0.002]
        self.L = 'map'
        self.format_of_map = "png"
        self.ll = [37.530887, 55.703118]
        self.map_api_server = "http://static-maps.yandex.ru/1.x/"
        self.initui()

    def initui(self):
        self.setWindowTitle("Map")
        self.setStyleSheet("QWidget {background: #00aaf1}")
        self.run()
        self.btn_map.clicked.connect(self.change_to_map)
        self.btn_map.setStyleSheet("QPushButton {background: green;}")
        self.btn_sat.clicked.connect(self.change_to_sat)
        self.btn_sat.setStyleSheet("QPushButton {background: green;}")
        self.btn_sat_skl.clicked.connect(self.change_to_sat_skl)
        self.btn_sat_skl.setStyleSheet("QPushButton {background: green;}")

    def change_to_map(self):
        self.L = "map"
        self.format_of_map = "png"
        self.map.setFocus()
        self.run()

    def change_to_sat(self):
        self.L = "sat"
        self.format_of_map = "jpg"
        self.map.setFocus()
        self.run()

    def change_to_sat_skl(self):
        self.L = "sat,skl"
        self.format_of_map = "jpg"
        self.map.setFocus()
        self.run()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.spn = [min(10.0, self.spn[0] + 0.001), min(10.0, self.spn[1] + 0.001)]
        elif event.key() == Qt.Key_PageDown:
            self.spn = [max(0, self.spn[0] - 0.001), max(0, self.spn[1] - 0.001)]
        elif event.key() == Qt.Key_Up:
            self.ll = [self.ll[0], self.ll[1] + 0.001]
        elif event.key() == Qt.Key_Down:
            self.ll = [self.ll[0], self.ll[1] - 0.001]
        elif event.key() == Qt.Key_Left:
            self.ll = [self.ll[0] - 0.001, self.ll[1]]
        elif event.key() == Qt.Key_Right:
            self.ll = [self.ll[0] + 0.001, self.ll[1]]
        self.run()

    def run(self):
        map_params = {
            "ll": f"{self.ll[0]},{self.ll[1]}",
            "spn": f"{self.spn[0]},{str(self.spn[1])}",
            "l": self.L
        }
        response = requests.get(self.map_api_server, params=map_params)
        self.map_file = f"map.{self.format_of_map}"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.map.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
