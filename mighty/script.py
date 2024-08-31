from typing import Any


class Config:
    """Settings / Configuration for the script."""

    def __init__(self) -> None:
        self.version: str = "1.0"
        self.randomness: float = 0.0
        self.delay: int = 100  # in milliseconds.

    def from_dict(self, data: dict[str, Any]) -> None:
        """Loads configuration data from a dictionary."""
        self.version = data.get("version", self.version)
        self.randomness = data.get("randomness", self.randomness)
        self.delay = data.get("delay", self.delay)

    def to_dict(self) -> dict[str, Any]:
        """Converts the configuration data to a dictionary."""
        return {
            "version": self.version,
            "randomness": self.randomness,
            "delay": self.delay
        }


class Script:
    """Stores configuration and script data."""

    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.config: Config = Config()
        self.code: list[str] = []

    @staticmethod
    def load_script(filename: str) -> 'Script':
        """Loads the script from file."""
        script = Script(filename)
        with open(filename, 'r') as file:
            lines = file.readlines()

        current_section = None
        script_lines = []
        settings = {}

        for line in lines:
            line = line.strip()

            # Skip empty lines and comments.
            if not line or line.startswith("#"):
                continue

            # Check for section headers.
            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1].lower()
                continue

            if current_section == "settings":
                # Parse settings in the form of key = value.
                key, value = map(str.strip, line.split("=", 1))
                if value.isdigit():
                    value = int(value)
                elif value.replace('.', '', 1).isdigit():
                    value = float(value)
                else:
                    value = value.strip('"')
                settings[key] = value

            elif current_section == "script":
                # Append script lines.
                script_lines.append(line)

        # Load settings and code into the script.
        script.config.from_dict(settings)
        script.code = script_lines

        return script

    def save_script(self) -> None:
        """Saves the script to a custom format file."""
        with open(self.filename, 'w') as file:
            # Write the settings section.
            file.write("[settings]\n")
            for key, value in self.config.to_dict().items():
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
            "y: float = 10.5",
            "print(x + y)",
            'print("Hello World!")'
        ]

        # Save the script with default settings.
        script.save_script()

        return script
