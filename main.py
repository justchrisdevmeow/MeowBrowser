import sys
from PyQt5.QtWidgets import QApplication
from window import MeowBrowser

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("MeowBrowser")
    
    window = MeowBrowser()
    window.show()
    
    sys.exit(app.exec_())
