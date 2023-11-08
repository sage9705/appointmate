import os
import sys
from PyQt5.QtWidgets import QApplication
from appointmate.ui.main_window import MainWindow
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from appointmate.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()