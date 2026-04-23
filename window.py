import os
import json
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon, QCursor, QPixmap
from PyQt5.QtWidgets import (QMainWindow, QLineEdit, QPushButton, QToolBar, 
                             QTabWidget, QMenuBar, QMenu, QAction, QStatusBar,
                             QVBoxLayout, QHBoxLayout, QListWidget, QDialog, 
                             QLabel, QMessageBox)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtMultimedia import QSound
from webview import MeowWebView
from cursors import CursorLoader
from bookmarks import BookmarkDialog

class MeowBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MeowBrowser")
        self.setGeometry(100, 100, 1200, 800)
        
        # Load cursors
        self.cursor_loader = CursorLoader()
        self.click_cursor = self.cursor_loader.click_cursor
        self.normal_cursor = self.cursor_loader.normal_cursor
        
        # Load bookmarks
        self.bookmarks_file = "bookmarks.json"
        self.bookmarks = self.load_bookmarks()
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.tab_changed)
        self.setCentralWidget(self.tabs)
        
        # Create UI
        self.create_menu_bar()
        self.create_toolbar()
        self.create_status_bar()
        
        # Create first tab
        self.new_tab()
        
        # Set initial cursor
        self.setCursor(self.normal_cursor)
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        new_tab_action = QAction("New Tab", self)
        new_tab_action.triggered.connect(self.new_tab)
        file_menu.addAction(new_tab_action)
        file_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Bookmarks menu
        self.bookmarks_menu = menubar.addMenu("Bookmarks")
        add_bookmark_action = QAction("Add Bookmark", self)
        add_bookmark_action.triggered.connect(self.add_bookmark)
        self.bookmarks_menu.addAction(add_bookmark_action)
        self.bookmarks_menu.addSeparator()
        self.update_bookmarks_menu()
        
        # View menu
        view_menu = menubar.addMenu("View")
        reload_action = QAction("Reload", self)
        reload_action.triggered.connect(self.reload_page)
        view_menu.addAction(reload_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        about_action = QAction("About MeowBrowser", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        nav_bar = QToolBar()
        self.addToolBar(nav_bar)
        
        # Navigation buttons
        back_btn = QPushButton("◀")
        back_btn.clicked.connect(self.go_back)
        nav_bar.addWidget(back_btn)
        
        forward_btn = QPushButton("▶")
        forward_btn.clicked.connect(self.go_forward)
        nav_bar.addWidget(forward_btn)
        
        reload_btn = QPushButton("⟳")
        reload_btn.clicked.connect(self.reload_page)
        nav_bar.addWidget(reload_btn)
        
        home_btn = QPushButton("🏠")
        home_btn.clicked.connect(self.go_home)
        nav_bar.addWidget(home_btn)
        
        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate)
        nav_bar.addWidget(self.url_bar)
        
        # Meow button
        meow_btn = QPushButton("😺 Meow")
        meow_btn.clicked.connect(self.meow_page)
        nav_bar.addWidget(meow_btn)
        
        # New tab button
        new_tab_btn = QPushButton("+")
        new_tab_btn.clicked.connect(self.new_tab)
        nav_bar.addWidget(new_tab_btn)
        
        # Bookmarks button
        bookmarks_btn = QPushButton("📖")
        bookmarks_btn.clicked.connect(self.show_bookmarks)
        nav_bar.addWidget(bookmarks_btn)
    
    def create_status_bar(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")
    
    def new_tab(self, url=None):
        browser = MeowWebView(self)
        if url is None:
            browser.setUrl(QUrl("https://www.google.com"))
        else:
            browser.setUrl(QUrl(url))
        
        browser.urlChanged.connect(lambda u, b=browser: self.update_tab_url(b, u))
        browser.loadFinished.connect(lambda _, b=browser: self.update_tab_title(b))
        browser.titleChanged.connect(lambda t, b=browser: self.update_tab_title(b))
        
        index = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(index)
        self.url_bar.setFocus()
    
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.get_current_browser().setUrl(QUrl("about:blank"))
    
    def get_current_browser(self):
        return self.tabs.currentWidget()
    
    def navigate(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://" + url
        self.get_current_browser().setUrl(QUrl(url))
    
    def go_back(self):
        self.get_current_browser().back()
    
    def go_forward(self):
        self.get_current_browser().forward()
    
    def reload_page(self):
        self.get_current_browser().reload()
    
    def go_home(self):
        self.get_current_browser().setUrl(QUrl("https://www.google.com"))
    
    def update_tab_url(self, browser, url):
        if browser == self.get_current_browser():
            self.url_bar.setText(url.toString())
        self.statusBar.showMessage(f"Loading: {url.toString()}", 2000)
    
    def update_tab_title(self, browser):
        index = self.tabs.indexOf(browser)
        if index != -1:
            title = browser.title()
            if len(title) > 20:
                title = title[:17] + "..."
            self.tabs.setTabText(index, title)
    
    def tab_changed(self, index):
        browser = self.get_current_browser()
        if browser:
            self.url_bar.setText(browser.url().toString())
    
    def meow_page(self):
        js = """
        function meowNode(node) {
            if (node.nodeType === Node.TEXT_NODE) {
                node.textContent = node.textContent.replace(/[a-zA-Z]+/g, 'meow');
            } else if (node.nodeType === Node.ELEMENT_NODE) {
                for (let child of node.childNodes) {
                    meowNode(child);
                }
            }
        }
        meowNode(document.body);
        """
        self.get_current_browser().page().runJavaScript(js)
        self.statusBar.showMessage("Meow! All text turned into meow.", 3000)
    
    def load_bookmarks(self):
        if os.path.exists(self.bookmarks_file):
            with open(self.bookmarks_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_bookmarks(self):
        with open(self.bookmarks_file, 'w') as f:
            json.dump(self.bookmarks, f)
    
    def add_bookmark(self):
        dialog = BookmarkDialog(self)
        current_url = self.get_current_browser().url().toString()
        dialog.url_input.setText(current_url)
        dialog.name_input.setText(self.get_current_browser().title() or current_url)
        
        if dialog.exec_():
            url = dialog.url_input.text()
            name = dialog.name_input.text()
            self.bookmarks.append({"name": name, "url": url})
            self.save_bookmarks()
            self.update_bookmarks_menu()
            self.statusBar.showMessage(f"Bookmarked: {name}", 3000)
    
    def update_bookmarks_menu(self):
        actions = self.bookmarks_menu.actions()
        for action in actions[2:]:
            self.bookmarks_menu.removeAction(action)
        
        for bookmark in self.bookmarks:
            action = QAction(bookmark["name"], self)
            action.setData(bookmark["url"])
            action.triggered.connect(lambda checked, url=bookmark["url"]: self.goto_bookmark(url))
            self.bookmarks_menu.addAction(action)
    
    def goto_bookmark(self, url):
        self.get_current_browser().setUrl(QUrl(url))
        self.statusBar.showMessage(f"Loading bookmark: {url}", 2000)
    
    def show_bookmarks(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Bookmarks")
        dialog.setModal(True)
        layout = QVBoxLayout()
        
        list_widget = QListWidget()
        for bookmark in self.bookmarks:
            list_widget.addItem(f"{bookmark['name']} - {bookmark['url']}")
        
        list_widget.itemDoubleClicked.connect(lambda item: self.goto_bookmark_from_list(item, dialog))
        
        layout.addWidget(list_widget)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.resize(400, 300)
        dialog.exec_()
    
    def goto_bookmark_from_list(self, item, dialog):
        text = item.text()
        url = text.split(" - ")[1]
        self.get_current_browser().setUrl(QUrl(url))
        dialog.close()
        self.statusBar.showMessage(f"Loading: {url}", 2000)
    
    def show_about(self):
        QMessageBox.about(self, "About MeowBrowser", 
                          "MeowBrowser v1.0\n\n"
                          "A cat-themed web browser with meow powers!\n\n"
                          "Features:\n"
                          "- Tabs\n"
                          "- Bookmarks\n"
                          "- Meow button (turns all text into 'meow')\n"
                          "- Dual paw cursors (left paw clicks, right paw points)\n\n"
                          "Made with ❤️ and meows")
    
    def closeEvent(self, event):
        self.save_bookmarks()
        event.accept()
