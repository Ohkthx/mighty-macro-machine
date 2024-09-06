from enum import Enum
from util import Vec2


class ActionType(Enum):
    """Types of actions taken by the user."""
    MPOS = "mpos"
    MCLICK = "mclick"
    MMOVE = "mmove"
    WAIT = "wait"


class Action:
    """Any action that can be taken by the script on behalf of the user."""

    def __init__(self, action_type: ActionType) -> None:
        self.type: ActionType = action_type
        self.is_done: bool = False


class Wait(Action):
    """Simulates a skipped frame with no activity."""

    def __init__(self, frames: int) -> None:
        super().__init__(ActionType.WAIT)
        self.frames = frames

    def __str__(self) -> str:
        return f"{self.type.value}({self.frames})"


class MousePosition(Action):
    """Current position the mouse should be in."""

    def __init__(self, position: Vec2) -> None:
        super().__init__(ActionType.MPOS)
        self.position: Vec2 = position

    def __str__(self) -> str:
        return f"{self.type.value}({self.position})"


class MouseMove(Action):
    """Instruct the mouse to move to the destination."""

    def __init__(self, position: Vec2, frames: int) -> None:
        super().__init__(ActionType.MMOVE)
        self.position = position
        self.frames = frames

    def __str__(self) -> str:
        return f"{self.type.value}({self.position}, {self.frames})"


class MouseClick(Action):
    """Records a mouse click event, either press or release."""

    def __init__(self, button: str, randomize: bool = False) -> None:
        super().__init__(ActionType.MCLICK)
        self.button = button
        self.randomize = randomize

    def __str__(self) -> str:
        return f"{self.type.value}(\"{self.button}\", {str(self.randomize).lower()})"
