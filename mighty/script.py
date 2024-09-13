from typing import Any


class GeneralConfig:
    """General configuration."""

    def __init__(self) -> None:
        self.version: str = "1.0"
        self.delay: int = 100  # in milliseconds.
        self.fps: int = 100  # Speed to record and playback.

    def from_dict(self, data: dict[str, Any]) -> None:
        """Loads configuration data from a dictionary."""
        self.version = data.get("version", self.version)
        self.delay = data.get("delay", self.delay)
        self.fps = data.get("fps", self.fps)

    def to_dict(self) -> dict[str, Any]:
        """Converts the configuration data to a dictionary."""
        return {
            "version": self.version,
            "delay": self.delay,
            "fps": self.fps,
        }


class MouseConfig:
    """Mouse specific configuration."""

    def __init__(self) -> None:
        self.smooth: bool = True
        self.randomness: float = 0.0

    def from_dict(self, data: dict[str, Any]) -> None:
        """Loads configuration data from a dictionary."""
        self.smooth = data.get("smooth", self.smooth)
        self.randomness = data.get("randomness", self.randomness)

    def to_dict(self) -> dict[str, Any]:
        """Converts the configuration data to a dictionary."""
        return {
            "smooth": self.smooth,
            "randomness": self.randomness,
        }


class KeyboardConfig:
    """Keyboard specific configuration."""

    def __init__(self) -> None:
        pass

    def from_dict(self, data: dict[str, Any]) -> None:
        """Loads configuration data from a dictionary."""
        pass

    def to_dict(self) -> dict[str, Any]:
        """Converts the configuration data to a dictionary."""
        return {}


class ScriptConfig:
    def __init__(self) -> None:
        self.general: GeneralConfig = GeneralConfig()
        self.mouse: MouseConfig = MouseConfig()
        self.keyboard: KeyboardConfig = KeyboardConfig()

    def from_dict(self, data: dict[str, Any]) -> None:
        """Loads configuration data from a dictionary."""
        if "general" in data:
            self.general.from_dict(data["general"])
        if "mouse" in data:
            self.mouse.from_dict(data["mouse"])
        if "keyboard" in data:
            self.keyboard.from_dict(data["keyboard"])

    def to_dict(self) -> dict[str, Any]:
        """Converts the configuration data to a dictionary."""
        return {
            "general": self.general.to_dict(),
            "mouse": self.mouse.to_dict(),
            "keyboard": self.keyboard.to_dict()
        }


class Script:
    """Stores configuration and script data."""

    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.config = ScriptConfig()
        self.code: list[str] = []

    @staticmethod
    def load_script(filename: str) -> 'Script':
        """Loads the script from file."""
        script = Script(filename)
        with open(filename, 'r') as file:
            lines = file.readlines()

        current_section = None
        script_lines = []
        settings = {"general": {}, "mouse": {}, "keyboard": {}}

        for line in lines:
            line = line.rstrip()

            # Skip empty lines and comments.
            if current_section != "script":
                line = line.lstrip()
                if not line or line.startswith("#"):
                    continue

            # Check for section headers.
            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1].lower()
                continue

            if current_section == "general-settings":
                # Parse settings in the form of key = value.
                key, value = map(str.strip, line.split("=", 1))
                value = Script._convert_value(value)
                settings["general"][key] = value

            elif current_section == "mouse-settings":
                # Parse settings in the form of key = value.
                key, value = map(str.strip, line.split("=", 1))
                value = Script._convert_value(value)
                settings["mouse"][key] = value

            elif current_section == "keyboard-settings":
                # Parse settings in the form of key = value.
                key, value = map(str.strip, line.split("=", 1))
                value = Script._convert_value(value)
                settings["keyboard"][key] = value

            elif current_section == "script":
                # Append script lines.
                script_lines.append(line)

        # Load settings and code into the script.
        script.config.from_dict(settings)
        script.code = script_lines

        return script

    @staticmethod
    def _convert_value(value: str) -> Any:
        """Converts a string value to its appropriate type."""
        if value.isdigit():
            return int(value)
        elif value.replace('.', '', 1).isdigit():
            return float(value)
        elif value.lower() in {"true", "false"}:
            return value.lower() == "true"
        else:
            return value.strip('"').strip("'")

    def save_script(self) -> None:
        """Saves the script to a custom format file."""
        with open(self.filename, 'w') as file:
            # Write the general settings section.
            file.write("[general-settings]\n")
            for key, value in self.config.general.to_dict().items():
                file.write(f"{key} = {repr(value)}\n")

            # Write the mouse settings section.
            file.write("\n[mouse-settings]\n")
            for key, value in self.config.mouse.to_dict().items():
                file.write(f"{key} = {repr(value)}\n")

            # Write the keyboard settings section.
            file.write("\n[keyboard-settings]\n")
            for key, value in self.config.keyboard.to_dict().items():
                file.write(f"{key} = {repr(value)}\n")

            # Write the script section.
            file.write("\n[script]\n")
            for line in self.code:
                file.write(f"{line}\n")

    def add_line(self, line: str) -> None:
        """Adds a line to the script code."""
        self.code.append(line)

    def parse_script(self) -> list[str]:
        """Parses the script lines to be processed by the interpreter."""
        return [line.strip() for line in self.code if line.strip()]

    @staticmethod
    def create_default(filename: str) -> 'Script':
        """Creates a script with default settings and saves it to the given file."""
        script = Script(filename)

        # Default code for the script.
        script.code = [
            "x: int = 5",
            "   -> y: float = 10.5",
            "print(x + y)",
            'print("Hello World!")',
            "",
            "func test(value: int) {",
            "   print(value)",
            "}",
            "",
            "test(x + x)"
        ]

        # Save the script with default settings.
        script.save_script()

        return script
