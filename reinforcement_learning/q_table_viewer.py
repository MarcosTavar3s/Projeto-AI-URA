from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QLabel, QFileDialog, QTableWidget, QTableWidgetItem, 
QVBoxLayout, QMessageBox)
from PyQt5.QtGui import QColor
import sys
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        layout = QVBoxLayout()
                
        # self.q_table = np.load("frozen/q_table_frozen_3000.npy")
        self.setWindowTitle("My App")
        
        self.upload_button = QPushButton("Select file")
        
        self.upload_button.setCheckable(True)
        self.upload_button.clicked.connect(self.upload_table)
        
        self.qlabel = QLabel("Q-Table viewer")
        self.qlabel.setStyleSheet("font-size: 20px; font-weight: bold;")

        
        # init of table widget    
        self.table = QTableWidget()
        self.table.setRowCount(3)  
        self.table.setColumnCount(3)     

        # layout
        for j in range(3):
            self.table.setColumnWidth(j, 200)  

        layout.addWidget(self.qlabel)
        layout.addWidget(self.table)
        layout.addWidget(self.upload_button)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
    def upload_table(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Select a file", "", "All files (*)")
        print(caminho)

        sucess = False

        try:
            self.q_table = np.load(caminho)
            sucess = True
        except Exception as e:
            QMessageBox.warning(self, "Error", "Try Again!\nError: "+str(e))
   
        if sucess:
            self.states, self.action = self.q_table.shape
            self.show_table()
            
            
        
    def show_table(self):
        self.table.clear()
        
        self.table.setRowCount(self.states)      # Número de linhas
        self.table.setColumnCount(self.action)   # Número de colunas
    
        for i in range(self.states):
            for j in range(self.action):
                item = QTableWidgetItem(str(round(self.q_table[i,j], 5)))
                self.table.setItem(i, j, item)
                
                try:
                    if self.q_table[i,j] > 0.5:
                        item.setBackground(QColor("#00EF04"))
                    elif self.q_table[i,j] < 0.05:
                        item.setBackground(QColor("#EF0000"))
                    else:
                        item.setBackground(QColor("#EFD300"))  
                except:
                    pass
   
app = QApplication(sys.argv)

window = MainWindow()
window.show()
window.showMaximized() 

# Start the event loop.
app.exec()
