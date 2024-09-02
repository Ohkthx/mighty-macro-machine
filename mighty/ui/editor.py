import threading
import time
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QPlainTextEdit, QShortcut
from PyQt5.QtGui import QFontMetrics, QKeySequence
from script import Script
from lang import Engine
from record import Recorder


class EditorTab(QWidget):
    """Provides the ability to edit scripts."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout for the editor tab.
        main_layout = QHBoxLayout()
        button_layout = QVBoxLayout()

        # Record button.
        self.record_button = QPushButton("Record")
        self.record_button.clicked.connect(self.record_script)
        self.record_button.setDisabled(True)
        button_layout.addWidget(self.record_button)

        # Playback button.
        self.playback_button = QPushButton("Playback")
        self.playback_button.clicked.connect(self.playback_script)
        self.playback_button.setDisabled(True)
        button_layout.addWidget(self.playback_button)

        # Save Changes button.
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_script)
        self.save_button.setDisabled(True)
        button_layout.addWidget(self.save_button)

        # Reset to last save button.
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_script)
        self.reset_button.setDisabled(True)
        button_layout.addWidget(self.reset_button)

        # Add a stretch to push the buttons to the top.
        button_layout.addStretch()

        # Right side for the script code editor.
        self.script_text_edit = QPlainTextEdit()
        self.script_text_edit.setReadOnly(False)

        # Set tab stop to 4 spaces wide.
        font_metrics = QFontMetrics(self.script_text_edit.font())
        tab_width = font_metrics.width(' ' * 4)  # Width of 4 spaces.
        self.script_text_edit.setTabStopDistance(tab_width)

        # Add the layouts to the main layout.
        main_layout.addLayout(button_layout, 1)  # 1/3 of the width.
        main_layout.addWidget(self.script_text_edit, 2)  # 2/3 of the width.

        # Set the main layout.
        self.setLayout(main_layout)

        # Initialize threading and stopping mechanism.
        self.thread = None
        self.stop_event = threading.Event()

        # Set up the shortcut for stopping the script (Ctrl+C).
        self.stop_shortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        self.stop_shortcut.activated.connect(self.stop_script)

    def load_script(self, script: Script):
        """Load the script's code into the editor."""
        self.script = script
        self.script_text_edit.setPlainText('\n'.join(self.script.code))
        self.record_button.setDisabled(False)
        self.playback_button.setDisabled(False)
        self.save_button.setDisabled(False)
        self.reset_button.setDisabled(False)

    def save_script(self):
        """Save the current content back into the scripts file."""
        self.script.code = self.script_text_edit.toPlainText().splitlines()
        self.script.save_script()

    def reset_script(self):
        """Reset the text box to the previously saved script content."""
        self.script_text_edit.setPlainText('\n'.join(self.script.code))

    def clear_editor(self):
        """Clear the editor when no script is selected."""
        self.script_text_edit.clear()
        self.record_button.setDisabled(True)
        self.playback_button.setDisabled(True)
        self.save_button.setDisabled(True)
        self.reset_button.setDisabled(True)

    def record_script(self):
        """Simulate recording text into the script editor."""
        self.record_button.setText("Stop")
        self.playback_button.setDisabled(True)
        self.record_button.clicked.disconnect()
        self.record_button.clicked.connect(self.stop_script)

        self.stop_event.clear()

        if self.thread and self.thread.is_alive():
            # Avoids duplicate threads.
            return

        self.thread = threading.Thread(target=self.run_record)
        self.thread.start()

    def playback_script(self):
        """Run the script in a separate thread."""
        self.playback_button.setText("Stop")
        self.record_button.setDisabled(True)
        self.playback_button.clicked.disconnect()
        self.playback_button.clicked.connect(self.stop_script)

        self.stop_event.clear()

        if self.thread and self.thread.is_alive():
            # Avoid duplicate threads.
            return

        self.thread = threading.Thread(target=self.run_script)
        self.thread.start()

    def run_script(self):
        """Method to run a simple loop in a separate thread, simulating playback."""
        try:
            engine = Engine(self.script.code, self.script.config.general.playback_fps)
            while not self.stop_event.is_set() and engine.next():
                pass
        except Exception as e:
            print(f"Error during playback: {e}")
        finally:
            self.stop_event.set()
            self.reset_buttons()

    def run_record(self):
        """Method to run a simple loop in a separate thread, simulating recording."""
        recorder: Recorder = Recorder(self.script.config.general.record_fps)
        try:
            while not self.stop_event.is_set():
                recorder.next()
        except Exception as e:
            print(f"Error during recording: {e}")
        finally:
            self.stop_event.set()
            self.script.code = recorder.actions
            self.script.save_script()
            self.reset_buttons()
            self.reset_script()

    def stop_script(self):
        """Stop the running script (either playback or recording)."""
        if self.thread and self.thread.is_alive():
            self.stop_event.set()
            self.thread.join(timeout=1)
        self.reset_buttons()

    def reset_buttons(self):
        """Reset buttons to their initial state."""
        self.record_button.setText("Record")
        self.playback_button.setText("Playback")
        self.record_button.setDisabled(False)
        self.playback_button.setDisabled(False)

        # Reconnect the original signals.
        self.record_button.clicked.disconnect()
        self.record_button.clicked.connect(self.record_script)

        self.playback_button.clicked.disconnect()
        self.playback_button.clicked.connect(self.playback_script)
