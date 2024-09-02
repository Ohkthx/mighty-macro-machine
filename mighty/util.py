class Vec2:
    """X, Y vector."""

    def __init__(self, position: tuple[int, int]) -> None:
        self.x = position[0]
        self.y = position[1]

    def __str__(self) -> str:
        return f"{self.x}, {self.y}"

    def __eq__(self, other) -> bool:
        if isinstance(other, Vec2):
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other) -> bool:
        if isinstance(other, Vec2):
            return (self.x, self.y) < (other.x, other.y)
        return NotImplemented

    def __le__(self, other) -> bool:
        if isinstance(other, Vec2):
            return (self.x, self.y) <= (other.x, other.y)
        return NotImplemented

    def __gt__(self, other) -> bool:
        if isinstance(other, Vec2):
            return (self.x, self.y) > (other.x, other.y)
        return NotImplemented

    def __ge__(self, other) -> bool:
        if isinstance(other, Vec2):
            return (self.x, self.y) >= (other.x, other.y)
        return NotImplemented
