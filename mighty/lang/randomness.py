import random


class Mouse:
    MOUSE_MIN_CLICK_MS: int = 55
    MOUSE_MAX_CLICK_MS: int = 135

    @staticmethod
    def click_time() -> float:
        """Amount of seconds to take for a click."""
        return random.randrange(Mouse.MOUSE_MIN_CLICK_MS, Mouse.MOUSE_MAX_CLICK_MS) / 1000
