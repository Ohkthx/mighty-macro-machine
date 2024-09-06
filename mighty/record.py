import time
from typing import Optional
from pynput import mouse
import pyautogui
from util import Vec2
from actions import Action, Wait, MousePosition, MouseClick


class Recorder:
    """Records the inputs the user is performing."""

    def __init__(self, interval_ms: int) -> None:
        self.interval = interval_ms
        self.last_mouse_pos: Optional[Vec2] = None
        self.inactive_frames: int = 0
        self.actions: list[str] = []
        self.last_click: Optional[str] = None

        # Start the mouse listener to track clicks.
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

    def on_click(self, x, y, button, pressed):
        """Handles mouse click events."""
        if pressed:
            # Record the button name when pressed.
            self.last_click = button.name

    def next(self) -> None:
        """Processes the next frame, pausing for the maximum of the interval time."""
        start = time.time()

        inputs: list[Action] = []

        # Obtain the inputs from the devices.
        inputs.extend(self.get_mouse())
        inputs.extend(self.get_keyboard())

        if len(inputs) > 0:
            if self.inactive_frames > 0:
                # Register the frames with no activity.
                self.actions.append(str(Wait(self.inactive_frames)))
                self.inactive_frames = 0

            # Convert to strings and mark them to execute on the same tick.
            actions = [str(action) for action in inputs]
            self.actions.append(str.join("\n\t-> ", actions))
        else:
            self.inactive_frames += 1

        # Calculate elapsed time and the required sleep time in seconds.
        sleep_time = (1.0 / self.interval) - (time.time() - start)

        if sleep_time > 0.0:
            time.sleep(sleep_time)

        return True

    def get_mouse(self) -> list[Action]:
        actions: list[Action] = []

        # Get the current mouse position.
        position = Vec2(pyautogui.position())
        if self.last_mouse_pos is None or self.last_mouse_pos != position:
            self.last_mouse_pos = position
            actions.append(MousePosition(position))

        # Record mouse clicks if any.
        if self.last_click is not None:
            actions.append(MouseClick(self.last_click))
            self.last_click = None  # Reset click after recording.

        return actions

    def get_keyboard(self) -> list[Action]:
        actions: list[Action] = []
        return actions
