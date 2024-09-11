from enum import Enum
from util import Vec2


class EventType(Enum):
    """Types of actions taken by the user."""
    MPOS = "mpos"
    MCLICK = "mclick"
    MMOVE = "mmove"
    WAIT = "wait"


class Event:
    """Any action that can be taken by the script on behalf of the user."""

    def __init__(self, action_type: EventType) -> None:
        self.type: EventType = action_type
        self.is_done: bool = False


class Wait(Event):
    """Simulates a skipped frame with no activity."""

    def __init__(self, frames: int) -> None:
        super().__init__(EventType.WAIT)
        self.frames: int = frames

    def __str__(self) -> str:
        return f"{self.type.value}({self.frames})"


class MousePosition(Event):
    """Current position the mouse should be in."""

    def __init__(self, position: Vec2) -> None:
        super().__init__(EventType.MPOS)
        self.position: Vec2 = position

    def __str__(self) -> str:
        return f"{self.type.value}({self.position})"


class MouseMove(Event):
    """Instruct the mouse to move to the destination."""

    def __init__(self, position: Vec2, frames: int) -> None:
        super().__init__(EventType.MMOVE)
        self.position: Vec2 = position
        self.frames: int = frames

    def __str__(self) -> str:
        return f"{self.type.value}({self.position}, {self.frames})"


class MouseClick(Event):
    """Records a mouse click event, either press or release."""

    def __init__(self, button: str, randomness: bool) -> None:
        super().__init__(EventType.MCLICK)
        self.button: str = button
        self.randomness: bool = randomness

    def __str__(self) -> str:
        return f"{self.type.value}(\"{self.button}\", {str(self.randomness).lower()})"
