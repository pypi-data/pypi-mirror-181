from contextlib import contextmanager


class VerbosePrintHandler:
    def __init__(self, start_msg, verbose=False):
        self.verbose = verbose
        if verbose:
            print(start_msg)
        self.exists_previous_message = False

    @contextmanager
    def print_msg(self, msg):
        if self.verbose:
            if self.exists_previous_message:
                print(f"\r├─ ")
            print(f"└─ {msg}...", end="")
        yield msg
        if self.verbose:
            print("DONE", end="")
            self.exists_previous_message = True
