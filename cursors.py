from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPixmap

class CursorLoader:
    def __init__(self):
        self.click_cursor = None
        self.normal_cursor = None
        self.load_cursors()
    
    def load_cursors(self):
        try:
            full_paw = QPixmap("resources/paw_cursor.png")
            if full_paw.isNull():
                raise FileNotFoundError("paw_cursor.png not found")
            
            width = full_paw.width()
            height = full_paw.height()
            
            # Split in half
            left_paw = full_paw.copy(0, 0, width // 2, height)
            right_paw = full_paw.copy(width // 2, 0, width // 2, height)
            
            # Scale to cursor size
            left_paw = left_paw.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            right_paw = right_paw.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Create cursors
            self.click_cursor = QCursor(left_paw, hotX=24, hotY=24)
            self.normal_cursor = QCursor(right_paw, hotX=24, hotY=24)
            
        except Exception as e:
            print(f"Could not load paw_cursor.png: {e}")
            self.click_cursor = QCursor(Qt.PointingHandCursor)
            self.normal_cursor = QCursor(Qt.ArrowCursor)
