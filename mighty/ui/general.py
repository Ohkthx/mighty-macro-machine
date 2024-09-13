import os
import re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from script import Script
from .script_controller import ScriptController


class GeneralTab(QWidget):
    """This tab is used to select scripts and modify their configurations."""

    def __init__(self, main_window: 'MainWindow', parent=None) -> None:
        super().__init__(parent)
        self.main_window = main_window  # Reference to MainWindow

        # Create the layout and sections.
        self.main_layout = QHBoxLayout()
        self.init_selection_section()
        self.init_settings_section()
        self.setLayout(self.main_layout)

        # Populate the script list with .mx3 files.
        self.populate_script_list()

    @property
    def script_controller(self) -> ScriptController:
        """Get the current ScriptController from the MainWindow."""
        return self.main_window.get_controller()

    def init_selection_section(self) -> None:
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
        self.save_button.clicked.connect(self.save_script)
        self.save_button.setDisabled(True)
        button_layout.addWidget(self.save_button)

        # Removes the script (has prompt.)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_script)
        self.delete_button.setDisabled(True)
        button_layout.addWidget(self.delete_button)

        # Add the button layout to the left layout.
        left_layout.addLayout(button_layout)

        # Add the left layout to the main layout.
        self.main_layout.addLayout(left_layout, 1)  # 1/3 of the width.

    def init_settings_section(self) -> None:
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

    def create_general_section(self) -> None:
        """Contains the general settings for the script."""
        group_box = QGroupBox("General")
        layout = QFormLayout()

        # A box to modify the delay before recording and playback.
        self.general_delay = QSpinBox()
        self.general_delay.setRange(0, 999999)
        self.general_delay.setSingleStep(100)
        layout.addRow(QLabel("Delay (ms):", self), self.general_delay)

        # Determines the speed in which recordings happen.
        self.general_fps = QSpinBox()
        self.general_fps.setRange(0, 999999)
        self.general_fps.setSingleStep(100)
        layout.addRow(QLabel("FPS:", self), self.general_fps)

        layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.setLabelAlignment(Qt.AlignLeft)

        group_box.setLayout(layout)
        return group_box

    def create_mouse_section(self) -> None:
        """Contains the mouse settings for the script."""
        group_box = QGroupBox("Mouse")
        layout = QFormLayout()

        # Checkbox to determine if movement should be smoothed out.
        self.mouse_smooth = QCheckBox()
        self.mouse_smooth.setDisabled(False)
        layout.addRow(QLabel("Smooth Movement:", self), self.mouse_smooth)

        # Randomness as a degree of imprecision when performing mouse actions.
        self.mouse_randomness = QDoubleSpinBox()
        self.mouse_randomness.setRange(0.00, 100.00)
        self.mouse_randomness.setDecimals(4)
        self.mouse_randomness.setSingleStep(0.001)
        self.mouse_randomness.setDisabled(False)
        layout.addRow(QLabel("Randomness:", self), self.mouse_randomness)

        layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.setLabelAlignment(Qt.AlignLeft)

        group_box.setLayout(layout)
        return group_box

    def create_keyboard_section(self) -> None:
        """Contains the keyboard settings for the script."""
        group_box = QGroupBox("Keyboard")
        layout = QFormLayout()

        self.keyboard_placeholder = QLabel("No keyboard settings yet.")
        layout.addRow(QLabel("Keyboard:", self), self.keyboard_placeholder)

        layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.setLabelAlignment(Qt.AlignLeft)

        group_box.setLayout(layout)
        return group_box

    def populate_script_list(self) -> None:
        """Populate the script list with .mx3 files found in the current directory."""
        self.script_list.clear()
        script_directory = os.getcwd()

        for filename in os.listdir(script_directory):
            if filename.endswith(".mx3"):
                self.script_list.addItem(filename)

        # Auto-select and highlight the first item if any scripts exist.
        if self.script_list.count() > 0:
            self.script_list.setCurrentRow(0)

    def load_script_settings(self, current_item) -> None:
        """Load the selected script's settings into the UI."""
        if not current_item:
            self.save_button.setDisabled(True)
            self.delete_button.setDisabled(True)
            return

        script_name = current_item.text()
        self.script_controller.load_script(script_name)

        config = self.script_controller.config()
        # Populate the General, Mouse, and Keyboard sections using script properties.
        self.general_delay.setValue(config.general.delay)
        self.general_fps.setValue(config.general.fps)
        self.mouse_smooth.setChecked(config.mouse.smooth)
        self.mouse_randomness.setValue(config.mouse.randomness)

        self.save_button.setDisabled(False)
        self.delete_button.setDisabled(False)

    def save_script(self) -> None:
        """Save the current settings back into the selected script."""
        if not self.script_controller._script:
            return

        script = self.script_controller.script()
        # Update the script object with the current UI settings.
        script.config.general.delay = self.general_delay.value()
        script.config.general.fps = self.general_fps.value()
        script.config.mouse.smooth = self.mouse_smooth.isChecked()
        script.config.mouse.randomness = self.mouse_randomness.value()

        # Save the script.
        script.save_script()

    def delete_script(self) -> None:
        """Delete the selected script after confirmation."""
        if not self.script_controller._script:
            return

        reply = QMessageBox.question(self, "Delete Script",
                                     f"Are you sure you want to delete the script '{
                                         self.script_controller.filename}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.script_controller.delete_script()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete the script: {e}")
                return

            current_item = self.script_list.currentItem()
            if current_item:
                self.script_list.takeItem(self.script_list.row(current_item))

            self.clear_settings_display()

            if self.script_list.count() > 0:
                self.script_list.setCurrentRow(0)
                self.delete_button.setDisabled(False)
                self.save_button.setDisabled(False)
            else:
                self.delete_button.setDisabled(True)
                self.save_button.setDisabled(True)

    def clear_settings_display(self) -> None:
        """Clear the settings display after deleting a script."""
        self.general_delay.setValue(0)
        self.general_fps.setValue(0)
        self.mouse_smooth.setChecked(False)
        self.mouse_randomness.setValue(0.000)
        self.keyboard_placeholder.setText("No keyboard settings yet.")
        self.save_button.setDisabled(True)
        self.delete_button.setDisabled(True)

    def create_new_script(self) -> None:
        """Create a new script after prompting for a valid name."""
        script_name, ok = QInputDialog.getText(self, "New Script", "Enter script name:")

        if ok and script_name:
            if not self.is_valid_filename(script_name):
                QMessageBox.warning(self, "Invalid Name", "The script name is invalid. Please try again.")
                return

            script_filename = script_name + ".mx3"
            script_path = os.path.join(os.getcwd(), script_filename)

            if os.path.exists(script_path):
                QMessageBox.warning(self, "File Exists",
                                    "A script with this name already exists. Please choose a different name.")
                return

            new_script = Script.create_default(script_path)
            new_script.save_script()
            self.script_controller.load_script(new_script.filename)

            self.script_list.addItem(script_filename)
            self.script_list.setCurrentItem(self.script_list.findItems(script_filename, Qt.MatchExactly)[0])

    def is_valid_filename(self, filename) -> None:
        """Check if the filename is valid (no special characters, etc.)."""
        return re.match(r'^[\w\s-]+$', filename) is not None
