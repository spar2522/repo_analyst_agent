import itertools
import threading
import time


class Spinner:

    def __init__(self, message):
        self.message = message
        self.running = False

    def start(self):

        self.running = True

        def spin():

            for c in itertools.cycle(["|", "/", "-", "\\"]):

                if not self.running:
                    break

                print(
                    f"\r{self.message} {c}",
                    end="",
                    flush=True,
                )

                time.sleep(0.1)

        self.thread = threading.Thread(target=spin)

        self.thread.start()

    def stop(self):

        self.running = False

        self.thread.join()

        print()
