class EngineParameters:
    """Configuration settings used to modify how the engine operates."""

    def __init__(self, fps: int, screen_size: tuple[int, int], mouse_randomness: float) -> None:
        self.screen_size = screen_size
        self.fps: int = fps
        self.mouse_randomness: float = mouse_randomness
