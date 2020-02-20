import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
import os
import sys
import requests
from PyQt5.QtGui import QPixmap, QColor, QPalette
from PyQt5.QtCore import Qt


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('map.ui', self)
        self.map.setFocus()
        self.spn = [0.002, 0.002]
        self.L = 'map'
        self.format_of_map = "png"
        self.pt = None
        self.ll = [37.530687, 55.703118]
        self.map_api_server = "http://static-maps.yandex.ru/1.x/"
        self.initui()

    def initui(self):
        self.setWindowTitle("Map")
        self.setStyleSheet("QWidget {background: #00aaff}")
        self.run()
        self.btn_map.clicked.connect(self.change_to_map)
        self.btn_map.setStyleSheet("QPushButton {background: green;}")
        self.btn_sat.clicked.connect(self.change_to_sat)
        self.btn_sat.setStyleSheet("QPushButton {background: green;}")
        self.btn_sat_skl.clicked.connect(self.change_to_sat_skl)
        self.btn_sat_skl.setStyleSheet("QPushButton {background: green;}")
        self.btn_search.clicked.connect(self.search)

    def search(self):
        try:
            toponym_to_find = self.line_to_search.text()
            geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
            geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": toponym_to_find,
                "format": "json"}
            response = requests.get(geocoder_api_server, params=geocoder_params)
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                "GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            self.ll = toponym_coodrinates.split(" ")
            self.pt = toponym_coodrinates.split(" ")
            self.run()
        except Exception:
            pass

    def change_to_map(self):
        self.L = "map"
        self.format_of_map = "png"
        self.run()

    def size(self, x1, y1, x2, y2):
        return [str(abs(float(x1) - float(x2))), str(abs(float(y1) - float(y2)))]

    def change_to_sat(self):
        self.L = "sat"
        self.format_of_map = "jpg"
        self.run()

    def change_to_sat_skl(self):
        self.L = "sat,skl"
        self.format_of_map = "jpg"
        self.run()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.spn = [min(10.0, self.spn[0] + 0.01), min(10.0, self.spn[1] + 0.01)]
        elif event.key() == Qt.Key_PageDown:
            self.spn = [max(0, self.spn[0] - 0.01), max(0, self.spn[1] - 0.01)]
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
        if self.pt:
            map_params = {
                "ll": f"{self.ll[0]},{self.ll[1]}",
                "spn": f"{self.spn[0]},{str(self.spn[1])}",
                "l": self.L,
                "pt": "{},pm2dgl".format(','.join(self.ll))
            }
        else:
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
