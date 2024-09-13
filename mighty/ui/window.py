from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget
from .script_controller import ScriptController
from .general import GeneralTab
from .editor import EditorTab
from .debug import DebugWindow


class MainWindow(QMainWindow):
    """This is the main window that is first launched when starting. It contains
    multiple tabs that allow the user to use the mighty language.
    """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Mighty Macro-Machine")

        # The currently loaded script.
        self.script_controller = ScriptController()

        # Create a main tab widget.
        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.on_tab_change)
        self.setCentralWidget(self.tabs)

        # Add a General tab and connect the signals.
        self.general = GeneralTab(self)
        self.tabs.addTab(self.general, "General")

        # Add the Editor tab.
        self.editor = EditorTab(self)
        self.tabs.addTab(self.editor, "Editor")

        # Add a Debug tab (This tab will not be shown, instead it will trigger the popup.)
        self.debug = QWidget()
        self.tabs.addTab(self.debug, "Debug")

        # Store the last active tab index.
        self.last_tab_index = 0

    def on_tab_change(self, index) -> None:
        """Handles the swap between different tabs."""
        if self.tabs.tabText(index) == "Debug":
            # Open the debug window, treating this as just a button.
            self.debug_window = DebugWindow()
            self.debug_window.show()

            # Set the tab back to the last active tab.
            self.tabs.setCurrentIndex(self.last_tab_index)
            return

        if self.tabs.tabText(index) == "Editor":
            self.editor.on_tab_focus()

        # Store the last active tab index.
        self.last_tab_index = index

    def get_controller(self) -> ScriptController:
        """Obtains the script controller belonging to the program."""
        return self.script_controller

    def update_controller(self, filename: str) -> None:
        """Has the controller update the script being controlled."""
        self.script_controller.load_script(filename)
