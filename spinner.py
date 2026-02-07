import threading
import itertools
import sys
import time


class Spinner:
    def __init__(self, message="Loading..."):
        self.message = message
        self.running = False
        self.thread: threading.Thread | None = None 

    def _spin(self):
        chars = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
        while self.running:
            sys.stdout.write(f"\r{next(chars)} {self.message}")
            sys.stdout.flush()
            time.sleep(0.1)

    def __enter__(self):
        self.running = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.start()
        return self

    def __exit__(self, *args):
        self.running = False
        if self.thread:
            self.thread.join()
        # Clear the spinner line completely
        sys.stdout.write("\r" + " " * (len(self.message) + 5) + "\r")
        sys.stdout.flush()
