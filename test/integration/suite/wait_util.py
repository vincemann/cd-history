import time
import unittest

TIMEOUT = 80


class WaitUtil:

    @staticmethod
    def wait_until(condition, target="finish"):
        start_time = time.time()
        while not condition():
            if time.time() - start_time > TIMEOUT:
                unittest.TestCase().fail(f"Timeout: Did not {target} within {TIMEOUT} seconds.")
            time.sleep(0.05)
