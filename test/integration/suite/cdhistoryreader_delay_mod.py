import time
from unittest.mock import MagicMock


class CdHistoryReaderDelayMod:

    def __init__(self, reader):
        self.reader = reader
        self.original_method = None

    def slow_down(self, delay):
        cd_history_reader = self.reader

        # Capture the original method before replacing it
        original_send_to_callback = cd_history_reader.send_dir_to_callback
        self.original_method = original_send_to_callback

        def side_effect(*args, **kwargs):
            # Use the original method with a delay
            time.sleep(delay)
            return original_send_to_callback(*args, **kwargs)

        # Replace the real method with the side effect function
        cd_history_reader.send_dir_to_callback = MagicMock(side_effect=side_effect)

    def reset_mock(self):
        self.reader.send_dir_to_callback = self.original_method
