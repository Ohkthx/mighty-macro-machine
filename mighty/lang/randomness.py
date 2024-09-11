import random


class Mouse:
    MOUSE_MIN_CLICK_MS: int = 55
    MOUSE_MAX_CLICK_MS: int = 135

    @staticmethod
    def click_time() -> float:
        """Amount of seconds to take for a click."""
        return random.randrange(Mouse.MOUSE_MIN_CLICK_MS, Mouse.MOUSE_MAX_CLICK_MS) / 1000

    @staticmethod
    def position(x: int, y: int, max_x: int, max_y: int, randomness: float) -> tuple[int, int]:
        """A randomized position based on a position around it."""
        x += int(random.uniform(-randomness, randomness) * max_x)
        y += int(random.uniform(-randomness, randomness) * max_y)

        # Ensure the new position doesn't go beyond max_x and max_y.
        x = max(0, min(x, max_x))
        y = max(0, min(y, max_y))

        return x, y
