import sys

from PyQt5 import QtWidgets, QtCore
from scapy.all import *

import sniffer_ui



pkt_list = {}



class SniffThread(QtCore.QThread):
    global pkt_list
    new_data = QtCore.pyqtSignal(str)

    def packethandler(self, pkt):
        if pkt.haslayer(Dot11)
            if pkt.type == 0 and pkt.subtype == 8 and str(pkt.info) not in pkt_list.keys():
                pkt_list[str(pkt.info)] = pkt.show(dump=True)
                self.new_data.emit(str(pkt.info))

    def run(self):
        sniff(iface='mon0', prn=self.packethandler)


class MainApp(QtWidgets.QMainWindow, sniffer_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.thread = SniffThread()
        self.thread.new_data.connect(self.append_new_item)
        self.thread.start()
        self.listWidget.itemClicked.connect(self.add_info)

    def append_new_item(self, data):
        self.listWidget.addItem(data)

    def add_info(self, key_dict):
        global pkt_list
        self.textBrowser.setText(pkt_list[key_dict.text()])


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
