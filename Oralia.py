import sys, mido
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from tab1 import Tab1
#
class Oralia(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabs = {}  # Dictionary to hold tab
        self.tab_widget = QTabWidget(self)  # QTabWidget object
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.West)
        self.setCentralWidget(self.tab_widget)
        self.tabs["Practical"] = Tab1(self.tab_widget)
        self.tab_widget.addTab(self.tabs["Practical"], "Practical")

app = QApplication([])
window = Oralia()
window.show()

with mido.open_input(callback=window.tabs["Practical"].midi_handling) as inport:
    sys.exit(app.exec())