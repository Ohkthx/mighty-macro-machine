import os
import signal
import threading
from typing import Optional, Callable
import pyautogui
from script import Script, ScriptConfig
from lang import Engine
from lang.params import EngineParameters
from record import Recorder


class ScriptController:
    def __init__(self, filename: Optional[str] = None) -> None:
        self.filename = filename
        self._script: Optional[Script] = None
        self._code: list[str] = []

        # Initialize threading and stopping mechanism.
        self.thread = None
        self.stop_event = threading.Event()
        self.stop_callback: Optional[Callable] = None

        # Set up signal handling for termination.
        signal.signal(signal.SIGTERM, self.stop_script)
        signal.signal(signal.SIGINT, self.stop_script)

    def script(self) -> Script:
        """Obtains the current script being controlled."""
        if self.script is None:
            raise Exception("Unable to load script configuration from controller, script is unset.")
        return self._script

    def code(self) -> list[str]:
        """Obtains the code for the script loaded."""
        return self.script().code

    def config(self) -> ScriptConfig:
        """Obtains the current configuration for the script loaded."""
        return self.script().config

    def load_script(self, filename: str) -> None:
        """Sets the script to be controlled."""
        self.filename = filename
        self.reset_script()

    def save_script(self) -> None:
        """Commits the current settings to the saved file."""
        self._script.code = self.code()
        self._script.save_script()

    def delete_script(self) -> None:
        """Deletes the script from existence."""
        if self._script is not None:
            os.remove(self._script.filename)

    def reset_script(self) -> None:
        """Loads the script from file resetting the settings."""
        self._script = Script.load_script(self.filename)
        self._code = self._script.code

    def set_stop_callback(self, call: Callable) -> None:
        """Sets the callback that will be used when script execution is halted."""
        self.stop_callback = call

    def stop_script(self) -> None:
        """Stop the running script (either playback or recording)."""
        if self.thread and self.thread.is_alive():
            self.stop_event.set()  # Signals the thread to stop,
            self.thread.join(timeout=1)  # Waits for the thread to stop.

            # Use the callback if one was set.
            if self.stop_callback is not None:
                self.stop_callback()
                self.stop_callback = None

    def record_script(self) -> None:
        """Records inputs and saves them to the currently controlled script."""
        self.stop_event.clear()

        if self.thread and self.thread.is_alive():
            # Avoids duplicate threads.
            return

        self.thread = threading.Thread(target=self.run_record)
        self.thread.daemon = True
        self.thread.start()

    def play_script(self) -> None:
        """Plays the currently controlled script."""
        self.stop_event.clear()

        if self.thread and self.thread.is_alive():
            # Avoid duplicate threads.
            return

        self.thread = threading.Thread(target=self.run_play)
        self.thread.daemon = True
        self.thread.start()

    def run_play(self) -> None:
        """Method to run a simple loop in a separate thread, simulating playback."""
        screen_size = pyautogui.size()
        config = self.config()
        params = EngineParameters(config.general.fps, screen_size, config.mouse.randomness)
        engine = Engine(self.code(), params)

        try:
            while not self.stop_event.is_set() and engine.next():
                pass
        except Exception as e:
            print(f"Error during playback: {e}")
        finally:
            self.stop_event.set()
            self.stop_callback()
            self.stop_callback = None

    def run_record(self) -> None:
        """Method to run a simple loop in a separate thread, simulating recording."""
        config = self.config()
        recorder: Recorder = Recorder(config.general.fps, config.mouse.randomness > 0.0)

        try:
            while not self.stop_event.is_set():
                recorder.next()
        except Exception as e:
            print(f"Error during recording: {e}")
        finally:
            self.stop_event.set()
            self._script.code = recorder.actions
            self.script().save_script()
            self.reset_script()
            self.stop_callback()
            self.stop_callback = None
