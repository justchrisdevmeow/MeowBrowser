from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MeowWebView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        
    def event(self, event):
        if event.type() == QEvent.CursorChange:
            cursor = self.cursor()
            if cursor.shape() == Qt.PointingHandCursor:
                self.main_window.setCursor(self.main_window.click_cursor)
            else:
                self.main_window.setCursor(self.main_window.normal_cursor)
        return super().event(event)
    
    def createWindow(self, windowType):
        if windowType == QWebEngineView.WebBrowserTab:
            self.main_window.new_tab()
            return self.main_window.get_current_browser()
        return super().createWindow(windowType)
