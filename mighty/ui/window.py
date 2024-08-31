from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget
from typing import Optional
from script import Script
from .general import GeneralTab
from .editor import EditorTab
from .debug import DebugWindow


class MainWindow(QMainWindow):
    """This is the main window that is first launched when starting. It contains
    multiple tabs that allow the user to use the mighty language.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mighty Macro-Machine")

        # The currently loaded script.
        self.script: Optional[Script] = None

        # Create a main tab widget.
        self.main_tabs = QTabWidget()
        self.main_tabs.currentChanged.connect(self.on_tab_change)
        self.setCentralWidget(self.main_tabs)

        # Add a General tab with subsections.
        self.general_tab = GeneralTab(self)
        self.general_tab.script_selected.connect(self.update_selected_script)  # Connect the signal
        self.main_tabs.addTab(self.general_tab, "General")

        # Add an Editor tab.
        self.editor_tab = EditorTab(self)
        self.main_tabs.addTab(self.editor_tab, "Editor")

        # Add a Debug tab (This tab will not be shown, instead it will trigger the popup)
        self.debug_tab = QWidget()
        self.main_tabs.addTab(self.debug_tab, "Debug")

        # Store the last active tab index.
        self.last_tab_index = 0

    def update_selected_script(self, script: Script):
        """Update the selected script across all relevant tabs."""
        self.script: Optional[Script] = script
        self.editor_tab.load_script(self.script)

    def on_tab_change(self, index):
        """Handles the swap between different tabs."""
        if self.main_tabs.tabText(index) == "Debug":
            # Open the debug window, treating this as just a button.
            self.debug_window = DebugWindow()
            self.debug_window.show()

            # Set the tab back to the last active tab.
            self.main_tabs.setCurrentIndex(self.last_tab_index)
        else:
            # Store the last active tab index.
            self.last_tab_index = index
