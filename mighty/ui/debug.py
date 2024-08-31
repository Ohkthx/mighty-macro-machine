from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer
import pyautogui
from PyQt5.QtGui import QKeyEvent, QKeySequence


class DebugWindow(QDialog):
    """"Shows helpful information when creating scripts."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Debug")

        # Layout for the Debug window.
        layout = QVBoxLayout()

        # Label to show mouse position.
        self.mouse_position_label = QLabel("Mouse Position: (0, 0)")
        layout.addWidget(self.mouse_position_label)

        # Label to show key presses.
        self.key_press_label = QLabel("Key Presses: None")
        layout.addWidget(self.key_press_label)

        self.setLayout(layout)

        # Set up a timer to update the mouse position.
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_mouse_position)
        self.timer.start(50)  # Update every 50 milliseconds.

    def update_mouse_position(self):
        """Updates the mouse position in the window."""
        x, y = pyautogui.position()
        self.mouse_position_label.setText(f"Mouse Position: ({x}, {y})")

    def keyPressEvent(self, event: QKeyEvent):
        """Updates the key the is currenting being pressed."""
        key = event.key()
        modifiers = event.modifiers()
        key_sequence = QKeySequence(modifiers | key)
        self.key_press_label.setText(f"Key Presses: {key_sequence.toString()}")

    def keyReleaseEvent(self, event: QKeyEvent):
        """"Clears the key that was just pressed."""
        self.key_press_label.setText("Key Presses: None")
