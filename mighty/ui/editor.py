from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QRect, pyqtSignal, QSize
from PyQt5.QtGui import QPainter, QFontMetrics
from .script_controller import ScriptController


class LineNumberArea(QWidget):
    """A widget that displays line numbers next to the code editor."""

    def __init__(self, editor) -> None:
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self) -> QSize:
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event) -> None:
        self.code_editor.line_number_area_paint_event(event)


class EditorTab(QWidget):
    """This tab allows for editing the script code."""
    on_code_save = pyqtSignal()  # Emits when the save button is pressed.

    def __init__(self, main_window: 'MainWindow', parent=None) -> None:
        super().__init__(parent)
        self.main_window = main_window

        # Initialize UI components.
        self.init_ui()

    @property
    def script_controller(self) -> ScriptController:
        """Get the current ScriptController from the MainWindow."""
        return self.main_window.get_controller()

    def init_ui(self) -> None:
        """Creates the UI elements such as the editor and buttons."""
        # Main layout for the editor tab.
        layout = QVBoxLayout(self)

        # Create the code editor widget with line numbers.
        self.code_editor = CodeEditor(self)
        layout.addWidget(self.code_editor)

        # Create the buttons layout (horizontal layout.)
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        # Add Record button.
        self.record_button = QPushButton("Record")
        self.record_button.clicked.connect(self.record_script)
        self.record_button.setFixedWidth(100)
        button_layout.addWidget(self.record_button)

        # Add Play button.
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_script)
        self.play_button.setFixedWidth(100)
        button_layout.addWidget(self.play_button)

        # Add button layout below the code editor.
        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Set the layout.
        self.setLayout(layout)

    def load_script_code(self) -> None:
        """Load the script code from the script controller."""
        self.code_editor.setPlainText("\n".join(self.script_controller.code()))

    def record_script(self) -> None:
        """When the record button is pressed."""
        self.record_button.setText("Stop")
        self.play_button.setDisabled(True)

        # Disconnect current behavior and reconnect to stop_script.
        self.record_button.clicked.disconnect()
        self.record_button.clicked.connect(self.script_controller.stop_script)

        self.script_controller.set_stop_callback(self.on_stop)
        self.script_controller.record_script()

    def play_script(self) -> None:
        """When the play button is pressed."""
        self.play_button.setText("Stop")
        self.record_button.setDisabled(True)

        # Disconnect current behavior and reconnect to stop_script.
        self.play_button.clicked.disconnect()
        self.play_button.clicked.connect(self.script_controller.stop_script)

        self.script_controller.set_stop_callback(self.on_stop)
        self.script_controller.play_script()

    def on_stop(self) -> None:
        """Handles the state reset when recording or playback is stopped."""
        # Reset button text.
        self.record_button.setText("Record")
        self.play_button.setText("Play")

        # Re-enable buttons.
        self.record_button.setDisabled(False)
        self.play_button.setDisabled(False)

        # Disconnect the stop functionality and reconnect the original behavior.
        self.record_button.clicked.disconnect()
        self.record_button.clicked.connect(self.record_script)

        self.play_button.clicked.disconnect()
        self.play_button.clicked.connect(self.play_script)

        self.on_tab_focus()

    def save_script_code(self) -> None:
        """Save the code currently in the editor to the script controller."""
        # Get the text from the code editor and split into lines.
        self.script_controller._code = self.code_editor.toPlainText().splitlines()
        self.script_controller.save_script()

    def on_tab_focus(self) -> None:
        """Called when this tab is focused, ensure we load the latest code."""
        self.load_script_code()


class CodeEditor(QPlainTextEdit):
    """A code editor with line numbers."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.line_number_area = LineNumberArea(self)

        # Connect updates for the line number area.
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)

        self.update_line_number_area_width(0)

        # Set up a monospaced font for the editor.
        font = self.document().defaultFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        self.setFont(font)
        self.setTabStopDistance(QFontMetrics(font).horizontalAdvance(' ') * 4)

    def line_number_area_width(self) -> int:
        """Calculates the width needed to display the line numbers."""
        digits = len(str(max(1, self.blockCount())))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _) -> None:
        """Updates the width of the line number area."""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy) -> None:
        """Repaint the line number area when necessary."""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event) -> None:
        """Handle resizing of the editor."""
        super().resizeEvent(event)

        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event) -> None:
        """Paint the line numbers in the margin."""
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.line_number_area.width(), self.fontMetrics().height(),
                                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def keyPressEvent(self, event) -> None:
        """Handle key presses (e.g., indenting.)"""
        super().keyPressEvent(event)
