import io
import time
import threading
import os


# mocks stdin buffer
# returns hardcoded strings on read
# supports multiple sequential reads
class DelayedInput(io.StringIO):
    def __init__(self, initial_value=""):
        super().__init__(initial_value)
        self.lock = threading.Lock()
        self.new_input_event = threading.Event()
        self.queue = []
        self.current_position = 0
        self.r_fd, self.w_fd = os.pipe()  # Create a pipe

    def fileno(self):
        return self.r_fd  # Return the read end of the pipe

    def readable(self):
        return True

    def read(self, *args, **kwargs):
        while True:
            self.new_input_event.wait()
            with self.lock:
                if self.current_position < len(self.queue):
                    data = self.queue[self.current_position]
                    self.current_position += 1
                    if self.current_position >= len(self.queue):
                        self.new_input_event.clear()
                    return data

    def readline(self, *args, **kwargs):
        return self.read(*args, **kwargs)

    def release_input(self, new_input):
        with self.lock:
            self.queue.append(new_input)
            self.new_input_event.set()  # Release the input
        os.write(self.w_fd, b'\n')  # Write to the pipe to make it selectable
