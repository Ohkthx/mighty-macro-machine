import os
import re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from script import Script


class GeneralTab(QWidget):
    """This tab is used to select scripts and modify their configurations."""
    script_selected = pyqtSignal(Script)  # Signal to emit when a script is selected.

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the layout and sections.
        self.main_layout = QHBoxLayout()
        self.init_selection_section()
        self.init_settings_section()
        self.setLayout(self.main_layout)

        # Populate the script list with .mx3 files.
        self.populate_script_list()

    def init_selection_section(self):
        """Creates the selection section (left-hand menu items.)"""
        # Selection box and action buttons layout.
        left_layout = QVBoxLayout()

        # Selection box for the script to interact with.
        self.script_list = QListWidget()
        self.script_list.setSelectionMode(QListWidget.SingleSelection)
        self.script_list.currentItemChanged.connect(self.load_script_settings)
        left_layout.addWidget(self.script_list)

        # Action buttons box.
        button_layout = QHBoxLayout()
        button_layout.setSpacing(3)

        # Used to create a new script.
        self.new_button = QPushButton("New")
        self.new_button.clicked.connect(self.create_new_script)
        button_layout.addWidget(self.new_button)

        # Saves to the selected script.
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_script_settings)
        self.save_button.setDisabled(True)
        button_layout.addWidget(self.save_button)

        # Removes the script (has prompt)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_script)
        self.delete_button.setDisabled(True)
        button_layout.addWidget(self.delete_button)

        # Add the button layout to the left layout
        left_layout.addLayout(button_layout)

        # Add the left layout to the main layout
        self.main_layout.addLayout(left_layout, 1)  # 1/3 of the width.

    def init_settings_section(self):
        """Creates the settings section (right-hand menu items.)"""
        self.settings_area = QWidget()
        self.settings_layout = QVBoxLayout()

        # Create sections for General, Mouse, and Keyboard.
        self.general_group = self.create_general_section()
        self.mouse_group = self.create_mouse_section()
        self.keyboard_group = self.create_keyboard_section()

        self.settings_layout.addWidget(self.general_group)
        self.settings_layout.addWidget(self.mouse_group)
        self.settings_layout.addWidget(self.keyboard_group)
        self.settings_area.setLayout(self.settings_layout)

        self.main_layout.addWidget(self.settings_area, 2)  # 2/3 of the width.

    def create_general_section(self):
        """Contains the general settings for the script."""
        group_box = QGroupBox("General")
        layout = QFormLayout()

        # A box to modify the delay before recording and playback.
        self.general_delay = QSpinBox()
        self.general_delay.setRange(0, 999999)
        self.general_delay.setSingleStep(100)
        layout.addRow(QLabel("Delay (ms):", self), self.general_delay)

        # Determines the speed in which recordings happen.
        self.general_record_fps = QSpinBox()
        self.general_record_fps.setRange(0, 999999)
        self.general_record_fps.setSingleStep(100)
        layout.addRow(QLabel("Record FPS:", self), self.general_record_fps)

        # Determines the speed in which playback happen.
        self.general_playback_fps = QSpinBox()
        self.general_playback_fps.setRange(0, 999999)
        self.general_playback_fps.setSingleStep(100)
        layout.addRow(QLabel("Playback FPS:", self), self.general_playback_fps)

        layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.setLabelAlignment(Qt.AlignLeft)

        group_box.setLayout(layout)
        return group_box

    def create_mouse_section(self):
        """Contains the mouse settings for the script."""
        group_box = QGroupBox("Mouse")
        layout = QFormLayout()

        # Checkbox to determine if movement should be smoothed out.
        self.mouse_smooth = QCheckBox()
        self.mouse_smooth.setDisabled(True)
        layout.addRow(QLabel("Smooth Movement:", self), self.mouse_smooth)

        # Polling speed controls the amount of frames the mouse moves at.
        self.mouse_polling = QSpinBox()
        self.mouse_polling.setRange(1, 2000)
        self.mouse_polling.setSingleStep(100)
        self.mouse_polling.setDisabled(True)
        layout.addRow(QLabel("Polling Speed (Hz):", self), self.mouse_polling)

        # Randomness as a degree of inprecision when performing mouse actions.
        self.mouse_randomness = QDoubleSpinBox()
        self.mouse_randomness.setRange(0.00, 100.00)
        self.mouse_randomness.setDecimals(2)
        self.mouse_randomness.setSingleStep(0.01)
        self.mouse_randomness.setDisabled(True)
        layout.addRow(QLabel("Randomness:", self), self.mouse_randomness)

        layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.setLabelAlignment(Qt.AlignLeft)

        group_box.setLayout(layout)
        return group_box

    def create_keyboard_section(self):
        """Contains the keyboard settings for the script."""
        group_box = QGroupBox("Keyboard")
        layout = QFormLayout()

        self.keyboard_placeholder = QLabel("No keyboard settings yet.")
        layout.addRow(QLabel("Keyboard:", self), self.keyboard_placeholder)

        layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.setLabelAlignment(Qt.AlignLeft)

        group_box.setLayout(layout)
        return group_box

    def populate_script_list(self):
        """Populate the script list with .mx3 files found in the current directory."""
        self.script_list.clear()
        script_directory = os.getcwd()  # Get the current working directory.

        for filename in os.listdir(script_directory):
            if filename.endswith(".mx3"):
                self.script_list.addItem(filename)

    def load_script_settings(self, current_item):
        """Load the selected scripts settings into the UI."""
        if not current_item:
            # Disable the save and delete buttons until a script is selected.
            self.save_button.setDisabled(True)
            self.delete_button.setDisabled(True)
            return

        script_name = current_item.text()
        script_path = os.path.join(os.getcwd(), script_name)
        self.script = Script.load_script(script_path)

        # Populate the General, Mouse, and Keyboard sections..
        self.general_delay.setValue(self.script.config.general.delay)
        self.general_record_fps.setValue(self.script.config.general.record_fps)
        self.general_playback_fps.setValue(self.script.config.general.playback_fps)

        # Mouse settings.
        self.mouse_smooth.setChecked(self.script.config.mouse.smooth)
        self.mouse_polling.setValue(self.script.config.mouse.polling_speed)
        self.mouse_randomness.setValue(self.script.config.mouse.randomness)

        # Keyboard settings.
        self.keyboard_placeholder.setText("No keyboard settings yet.")  # Placeholder

        # Enable the save and delete buttons when a script is selected.
        self.save_button.setDisabled(False)
        self.delete_button.setDisabled(False)

        # Emit the signal to notify the MainWindow about the selected script
        self.script_selected.emit(self.script)

    def save_script_settings(self):
        """Save the current settings back into the selected script."""
        if not self.script:
            return

        # Update the script object with the current UI settings.
        self.script.config.general.delay = self.general_delay.value()
        self.script.config.general.record_fps = self.general_record_fps.value()
        self.script.config.general.playback_fps = self.general_playback_fps.value()
        self.script.config.mouse.smooth = self.mouse_smooth.isChecked()
        self.script.config.mouse.polling_speed = self.mouse_polling.value()
        self.script.config.mouse.randomness = self.mouse_randomness.value()

        # Push the changes to the actual script.
        self.script.save_script()

        # Confirmation message.
        # QMessageBox.information(self, "Saved", "The script settings have been saved successfully.")

    def delete_script(self):
        """Delete the selected script after confirmation."""
        if not self.script:
            return

        reply = QMessageBox.question(self, "Delete Script",
                                     f"Are you sure you want to delete the script '{self.script.filename}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            script_path = self.script.filename

            # Remove the script file.
            try:
                os.remove(script_path)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete the script: {e}")
                return

            # Remove the script from the list.
            current_item = self.script_list.currentItem()
            if current_item:
                self.script_list.takeItem(self.script_list.row(current_item))

            # Clear the settings display.
            self.clear_settings_display()

            # Confirmation message.
            # QMessageBox.information(self, "Deleted", "The script has been deleted successfully.")

    def clear_settings_display(self):
        """Clear the settings display after deleting a script."""
        self.general_delay.setValue(0)
        self.general_record_fps.setValue(0)
        self.general_playback_fps.setValue(0)
        self.mouse_smooth.setChecked(False)
        self.mouse_polling.setValue(1)
        self.mouse_randomness.setValue(0.00)
        self.keyboard_placeholder.setText("No keyboard settings yet.")

        # Disable the save and delete buttons.
        self.save_button.setDisabled(True)
        self.delete_button.setDisabled(True)

    def create_new_script(self):
        """Create a new script after prompting for a valid name."""
        script_name, ok = QInputDialog.getText(self, "New Script", "Enter script name:")

        if ok and script_name:
            # Validate the script name.
            if not self.is_valid_filename(script_name):
                QMessageBox.warning(self, "Invalid Name", "The script name is invalid. Please try again.")
                return

            script_filename = script_name + ".mx3"
            script_path = os.path.join(os.getcwd(), script_filename)

            # Check if file already exists.
            if os.path.exists(script_path):
                QMessageBox.warning(self, "File Exists",
                                    "A script with this name already exists. Please choose a different name.")
                return

            # Create the new script.
            new_script = Script.create_default(script_path)
            new_script.save_script()

            # Add the new script to the list and select it.
            self.script_list.addItem(script_filename)
            self.script_list.setCurrentItem(self.script_list.findItems(script_filename, Qt.MatchExactly)[0])

    def is_valid_filename(self, filename):
        """Check if the filename is valid (no special characters, etc.)."""
        # Allow alphanumeric characters, underscores, dashes, and spaces.
        return re.match(r'^[\w\s-]+$', filename) is not None
