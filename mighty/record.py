import time
from typing import Optional
from pynput import mouse
import pyautogui
from util import Vec2
from event import Event, Wait, MousePosition, MouseClick


class Recorder:
    """Records the inputs the user is performing."""

    def __init__(self, interval_ms: int, mouse_randomness: bool) -> None:
        self.interval: int = interval_ms
        self.mouse_randomness: bool = mouse_randomness
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

        events: list[Event] = []

        # Obtain the inputs from the devices.
        events.extend(self.get_mouse())
        events.extend(self.get_keyboard())

        if len(events) > 0:
            if self.inactive_frames > 0:
                # Register the frames with no activity.
                self.actions.append(str(Wait(self.inactive_frames)))
                self.inactive_frames = 0

            # Convert to strings and mark them to execute on the same tick.
            actions = [str(event) for event in events]
            self.actions.append(str.join("\n\t-> ", actions))
        else:
            self.inactive_frames += 1

        # Calculate elapsed time and the required sleep time in seconds.
        sleep_time = (1.0 / self.interval) - (time.time() - start)

        if sleep_time > 0.0:
            time.sleep(sleep_time)

        return True

    def get_mouse(self) -> list[Event]:
        events: list[Event] = []

        # Get the current mouse position.
        position = Vec2(pyautogui.position())
        if self.last_mouse_pos is None or self.last_mouse_pos != position:
            self.last_mouse_pos = position
            events.append(MousePosition(position))

        # Record mouse clicks if any.
        if self.last_click is not None:
            events.append(MouseClick(self.last_click, self.mouse_randomness))
            self.last_click = None  # Reset click after recording.

        return events

    def get_keyboard(self) -> list[Event]:
        events: list[Event] = []
        return events
