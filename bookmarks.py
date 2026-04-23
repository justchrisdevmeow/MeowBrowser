from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

class BookmarkDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Bookmark")
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        self.url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        
        buttons = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(ok_btn)
        buttons.addWidget(cancel_btn)
        
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addLayout(buttons)
        
        self.setLayout(layout)
