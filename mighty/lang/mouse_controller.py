from enum import Enum
from typing import Optional
import time
import random
import pyautogui

"""Represents a point in a 2D space."""
Point = tuple[int, int]


class MouseButton(Enum):
    """Valid mouse buttons."""
    LEFT = 'left'
    RIGHT = 'right'
    MIDDLE = 'middle'


class ButtonState(Enum):
    """Valid states for each button."""
    UP = 'Up'
    DOWN = 'Down'


class MouseController:
    MOUSE_MIN_CLICK_MS: int = 55
    MOUSE_MAX_CLICK_MS: int = 135

    def __init__(self) -> None:
        # Initialize button states and position.
        self.mouse_buttons: dict[MouseButton, ButtonState] = {button: ButtonState.UP for button in MouseButton}
        self.cursor_position: Optional[Point] = pyautogui.position()

    def update_state(self, button_name: MouseButton, state: ButtonState) -> None:
        """Update the state of a mouse button."""
        self.mouse_buttons[button_name] = state

    def update_position(self) -> None:
        """Update the stored cursor position."""
        position = pyautogui.position()
        if position is not None:
            self.cursor_position = position

    def cursor_moved(self, x: int, y: int) -> bool:
        """Checks to see if the mouse cursor has moved from prior location."""
        return self.cursor_position and (x != self.cursor_position[0] or y != self.cursor_position[1])

    def click_button(self, button: MouseButton, randomize: bool) -> None:
        """Simulate a click using pyautogui."""
        pyautogui.mouseDown(button=button.value, _pause=False)
        self.update_state(button, ButtonState.DOWN)

        if randomize:
            # Used to simulate semi-realistic time for click speed.
            time.sleep(MouseController.click_time())

        pyautogui.mouseUp(button=button.value, _pause=False)
        self.update_state(button, ButtonState.UP)

    def move_cursor(self, x: int, y: int) -> None:
        """Moves the mouse cursor to the x, y position."""
        if self.cursor_moved(x, y):
            pyautogui.moveTo(x, y, _pause=False)
            self.cursor_position = (x, y)

    @staticmethod
    def click_time() -> float:
        """Amount of seconds to take for a click."""
        return random.randrange(MouseController.MOUSE_MIN_CLICK_MS, MouseController.MOUSE_MAX_CLICK_MS) / 1000
