import itertools
import threading
import time


class Spinner:
    """A class for displaying a spinning animation in the console to indicate ongoing processes."""

    SPINNER_CHARS = ["|", "/", "-", "\\"]  # Class-level constant for spinner characters

    def __init__(self, message):
        """
        Initialize the Spinner with a message to display alongside the spinner.

        :param message: The message to display before the spinner.
        """
        self.message = message
        self.running = False
        self.thread = None

    def start(self):
        """
        Start the spinner animation in a separate thread.

        Raises:
            RuntimeError: If the spinner is already running.
        """
        if self.running:
            raise RuntimeError("Spinner is already running.")

        self.running = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.start()

    def stop(self):
        """
        Stop the spinner animation and clear the line.
        """
        if not self.running:
            return

        self.running = False
        if self.thread is not None:
            self.thread.join()

        # Clear the line after the spinner stops
        print()

    def _spin(self):
        """
        Internal method to handle the spinning animation loop.
        """
        try:
            for char in itertools.cycle(Spinner.SPINNER_CHARS):
                if not self.running:
                    break

                print(
                    f"\r{self.message} {char}",
                    end="",
                    flush=True,
                )
                time.sleep(0.1)
        except Exception as e:
            # Handle any exceptions that occur during spinning
            print(f"\nError in spinner: {e}")
            self.running = False