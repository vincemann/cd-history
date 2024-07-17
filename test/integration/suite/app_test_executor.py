import multiprocessing
import os
import signal
import sys
import threading
import traceback


class TestExecutor:

    def __init__(self, app):
        self.app = app
        self.process = None

    def send_sigint(self):
        os.kill(self.process.pid, signal.SIGINT)

    # runs my test in separate thread to tkinter can run in main thread
    # propagates exception into main thread for unittest to catch
    # also runs the test in a whole separate process to ensure max isolation
    # (some shared state f's with my test suite so this is needed for now)
    # you can pass stdin mock DelayedInput object to the downstream process
    # thus mocking the stdin of the process
    def start_test_in_process(self, runnable, stdin=None):
        exception_queue = multiprocessing.Queue()

        def process(stdin_input, exception_queue):
            def test():
                try:
                    # Assign the DelayedInput instance to sys.stdin in the subprocess
                    sys.stdin = stdin_input
                    runnable()
                except Exception as e:
                    exception_queue.put((e, traceback.format_exc()))

            thread = threading.Thread(target=test)
            thread.start()
            # start app on main thread
            self.app.start()
            thread.join()

        process = multiprocessing.Process(target=process, args=(stdin, exception_queue))
        self.process = process
        process.start()
        while process.is_alive():
            if not exception_queue.empty():
                process.terminate()
                process.join()
                self.raise_exception(exception_queue)

        if not exception_queue.empty():
            self.raise_exception(exception_queue)

    def raise_exception(self, queue):
        e, trace = queue.get()
        print("An exception occurred during the test:")
        print(trace)
        raise e

    # starts test in same process, but run my test in diff thread, so code under test
    # can run on main (required by tkinter)
    def start_test(self, runnable):
        exception = None

        def test():
            nonlocal exception
            try:
                runnable()
            except Exception as e:
                exception = e

        thread = threading.Thread(target=test)
        thread.start()
        # start app on main thread
        self.app.start()
        thread.join()

        if exception:
            raise exception
