from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QPlainTextEdit
from PyQt5.QtGui import QFontMetrics
from script import Script


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
        recorded_text = "This is a recorded script."
        self.script_text_edit.setPlainText(recorded_text)

    def playback_script(self):
        """Simulate playing back the text from the script editor."""
        script_content = self.script_text_edit.toPlainText()
        print(f"Playing back script: {script_content}")
