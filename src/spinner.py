import threading
import itertools
import sys
import time


class Spinner:
    """
    A context manager that displays a loading spinner animation.

    Usage:
        with Spinner("Loading..."):
            # do work
    """

    def __init__(self, message: str = "Loading..."):
        """
        Initialize the spinner.

        Args:
            message: Text to display next to the spinner
        """
        self.message = message
        self.running = False
        self.thread: threading.Thread | None = None

    def _spin(self):
        """Internal method that runs the spinner animation loop."""
        chars = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
        while self.running:
            sys.stdout.write(f"\r{next(chars)} {self.message}")
            sys.stdout.flush()
            time.sleep(0.1)

    def __enter__(self):
        """Start the spinner when entering the context."""
        self.running = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.start()
        return self

    def __exit__(self, *args):
        """Stop the spinner and clean up when exiting the context."""
        self.running = False
        if self.thread:
            self.thread.join()
        # Clear the spinner line completely
        sys.stdout.write("\r" + " " * (len(self.message) + 5) + "\r")
        sys.stdout.flush()
