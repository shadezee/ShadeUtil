from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QStyleFactory, QPushButton, QLabel, QCheckBox, QTextEdit, QMessageBox
from utils.m_network_fix import *
from utils.m_clear_temp_files import *
from utils.support.m_run_as_admin import *
from utils.support.helpers import *

class GUI(QWidget):
    recycle = True;

    def __init__(self):
        super().__init__()
        self.initGUI()

    def initGUI(self):
        self.setWindowTitle("Shade Utils")
        self.setFixedSize(480, 600)
        layout = QVBoxLayout(self)

        # CREATE WIDGET 
        self.button_network_fix = QPushButton('Fix Wi-fi')
        self.button_clear_temp = QPushButton('Clean Temporary Files Folder')
        self.button_clear_temp_permanently = QPushButton('Recycle?')
        self.info_terminal = QTextEdit()
        self.display_terminal = QTextEdit()
        self.clear_terminal = QPushButton('Clear Display')

        # WIDGET CONFIGS
        self.button_clear_temp_permanently.setStyleSheet('background-color : #acd42a')
        self.info_terminal.setReadOnly(True)
        self.info_terminal.setFixedSize(480, 50)
        self.display_terminal.setReadOnly(True)
        scrollbar = self.display_terminal.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

        # SET WIDGET AVAILABILITY
        self.button_network_fix.setEnabled(True)
        self.button_clear_temp.setEnabled(True)
        self.button_clear_temp_permanently.setEnabled(True)
        self.clear_terminal.setEnabled(True)

        # SET LAYOUT
        layout.addWidget(self.button_network_fix)
        layout.addWidget(self.button_clear_temp)
        layout.addWidget(self.button_clear_temp_permanently)
        layout.addWidget(self.info_terminal)
        layout.addWidget(self.display_terminal)
        layout.addWidget(self.clear_terminal)

        # SET WIDGET FUNCTIONALITY
        self.button_network_fix.clicked.connect(self.fix_wifi)
        self.button_clear_temp.clicked.connect(self.clear_temp_files)
        self.button_clear_temp_permanently.clicked.connect(self.toggle_clean_temp_status)
        self.clear_terminal.clicked.connect(self.clear_display_terminal)

        # CALL INITIAL FUNCTIONS
        self.get_sizes()

    def get_sizes(self):
        result_temp = get_temp_folder_size()
        result_rec = get_recycle_bin_size()
        self.info_terminal.setPlainText(
            f'Temp folder size: {result_temp:.2f} MB.\n'
            f'Recycle bin size: {result_rec:.2f} MB.'
        )

    def fix_wifi(self):
        run_as_admin_user()
        result = network_fix()
        if (result):
            self.display_terminal.setPlainText(f'Driver successfully reset.')
        else:
            self.display_terminal.setPlainText(f'Error encountered: {result}.')

    def clear_temp_files(self):
        text = self.display_terminal.toPlainText()
        self.display_terminal.setPlainText(f"{text}\nCleaning...")

        result = clean_temp_folder(self.recycle)
        text = self.display_terminal.toPlainText()

        self.display_terminal.setPlainText(f"{text}\nThe following items were not cleaned: ")
        for item in result:
            text = self.display_terminal.toPlainText()
            self.display_terminal.setPlainText(f"{text}\n{item}")

        self.get_sizes()

    def show_temp_folder(self):
        open_temp()

    def toggle_clean_temp_status(self):
        self.recycle = not self.recycle
        if(self.recycle):
            self.button_clear_temp_permanently.setStyleSheet('background-color : #acd42a')
        else:
            self.button_clear_temp_permanently.setStyleSheet('background-color : #f92672')

    def clear_display_terminal(self):
        self.display_terminal.clear()

    def popup(self):
        box = QMessageBox()

if __name__ == "__main__":
    app = QApplication([])
    gui = GUI()
    gui.show()
    app.exec()
