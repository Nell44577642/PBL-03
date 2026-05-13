from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QComboBox, QLineEdit, QPushButton, QTextEdit, QLabel, QGroupBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class MetroView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ESME Best Route")
        self.setGeometry(100, 100, 1200, 800)
        
        self.city_selector = QComboBox()
        cities = [("Paris", "paris.json"), ("Bordeaux", "bordeaux.json"), ("Lille", "lille.json"), ("Lyon", "lyon.json"), ("Test", "mini_reseau.json")]
        for name, filename in cities: self.city_selector.addItem(name, filename)
        
        self.start_input = QLineEdit(); self.end_input = QLineEdit()
        self.btn_calculate = QPushButton("CALCULATE ROUTE")
        
        self.close_st_input = QLineEdit(); self.btn_close_st = QPushButton("Close Station")
        self.close_line_input = QLineEdit(); self.btn_close_line = QPushButton("Close Line")
        self.btn_reset_disruptions = QPushButton("Reset All")

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("background-color: #0c0c0c; color: #dcdcdc; font-family: Consolas; font-size: 10pt;")
        
        self.figure = plt.figure(); self.canvas = FigureCanvas(self.figure)
        self._setup_layout()

    def _setup_layout(self):
        central = QWidget(); self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        left_col = QVBoxLayout()
        
        search_box = QGroupBox("Route Finder")
        s_lay = QVBoxLayout(); s_lay.addWidget(self.city_selector)
        row = QHBoxLayout(); row.addWidget(self.start_input); row.addWidget(self.end_input)
        s_lay.addLayout(row); s_lay.addWidget(self.btn_calculate)
        search_box.setLayout(s_lay); left_col.addWidget(search_box)

        disrupt_box = QGroupBox("Disruptions")
        d_lay = QVBoxLayout()
        r1 = QHBoxLayout(); r1.addWidget(self.close_st_input); r1.addWidget(self.btn_close_st)
        r2 = QHBoxLayout(); r2.addWidget(self.close_line_input); r2.addWidget(self.btn_close_line)
        d_lay.addLayout(r1); d_lay.addLayout(r2); d_lay.addWidget(self.btn_reset_disruptions)
        disrupt_box.setLayout(d_lay); left_col.addWidget(disrupt_box)

        left_col.addWidget(self.console)
        main_layout.addLayout(left_col, 1)
        main_layout.addWidget(self.canvas, 2)