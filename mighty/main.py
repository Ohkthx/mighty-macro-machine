import sys
from PyQt5.QtWidgets import QApplication
from ui.window import MainWindow


def main():
    """Main entry point of the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
