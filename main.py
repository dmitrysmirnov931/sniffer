from scapy.all import *
import sniffer_ui
from PyQt5 import QtWidgets, QtCore
import sys


pkt_list = {}  # Создаем словарь для хранения пар: (название точки доступа:подробная информация)


# Объявляем класс, наследовав его от QThread, чтобы выполнять сниффинг, не блокируя при этом GUI:
class SniffThread(QtCore.QThread):
    global pkt_list
    new_data = QtCore.pyqtSignal(str)

    def packethandler(self, pkt):  # В потоке создаем обработчик пакетов
        if pkt.haslayer(Dot11):  # Проверяем, что в полученном пакете есть слой стандарта IEEE 802.11(Wi-Fi)
            # В стандарте IEEE 802.11, beacon-фреймы обладают типом номер 0(management) и подтипом номер 8(beacon):
            if pkt.type == 0 and pkt.subtype == 8 and str(pkt.info) not in pkt_list.keys():
                # Параметр dump=True указывает на то, чтобы функция выводила информацию о пакете в return, а не print:
                pkt_list[str(pkt.info)] = pkt.show(dump=True)
                self.new_data.emit(str(pkt.info))

    def run(self):
        sniff(iface='mon0', prn=self.packethandler)


class MainApp(QtWidgets.QMainWindow, sniffer_ui.Ui_MainWindow):  # Объявляем класс главного окна
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.thread = SniffThread()  # Создаем экземпляр класса SniffThread, объявленного ранее
        self.thread.new_data.connect(self.append_new_item)  # Передаем сигнал из потока в функцию append_new_item
        self.thread.start()  # Запускаем поток
        self.listWidget.itemClicked.connect(self.add_info)  # Привязываем событие listWidget.itemClicked к add_info

    def append_new_item(self, data):
        self.listWidget.addItem(data)  # Добавляем SSID найденных точек доступа в listWidget

    def add_info(self, key_dict):
        global pkt_list
        # Добавляем дополнительную информацию о точке доступа в textBrowser:
        self.textBrowser.setText(pkt_list[key_dict.text()])


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()  # Создаем экземпляр класса главного окна
    window.show()  # Выводим главное окно на экран
    app.exec_()


if __name__ == '__main__':  # Запускаем приложение из терминала
    main()
