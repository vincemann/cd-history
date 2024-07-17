import textwrap
import unittest
import tempfile
import os
from unittest.mock import MagicMock, call

from cd_history.cd_history_reader import CdHistoryReader


class TestCdHistoryReader(unittest.TestCase):

    def setUp(self):
        self.mock_callback = MagicMock()

    def create_test_file(self, content):
        self.test_history_file = tempfile.NamedTemporaryFile(delete=False)
        self.test_history_file.write(bytes(content, "utf-8"))
        self.test_history_file.close()

    def create_reader(self, max_lines):
        return CdHistoryReader(self.test_history_file.name, max_lines, self.mock_callback)

    def tearDown(self):
        # Remove the temporary file after the test
        os.unlink(self.test_history_file.name)

    def test_find_n_recent_dirs(self):
        # given
        history = textwrap.dedent(f"""
            /home/user/documents
            /home/user/downloads
            /home/user/foo
            /home/user/bar
        """).strip()
        self.create_test_file(history)
        max_lines = 3
        reader = self.create_reader(max_lines)

        # when
        reader.read()

        # then
        expected_calls = [
            call('/home/user/bar'),
            call('/home/user/foo'),
            call('/home/user/downloads'),
        ]
        self.mock_callback.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(3, self.mock_callback.call_count)

    def test_find_all_recent_dirs(self):
        # given
        history = textwrap.dedent(f"""
            /home/user/documents
            /home/user/downloads
            /home/user/foo
            /home/user/bar
        """).strip()
        self.create_test_file(history)
        max_lines = -1
        reader = self.create_reader(max_lines)

        # when
        reader.read()

        # then
        expected_calls = [
            call('/home/user/bar'),
            call('/home/user/foo'),
            call('/home/user/downloads'),
            call('/home/user/documents'),
        ]
        self.mock_callback.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(4, self.mock_callback.call_count)

    def test_history_with_some_newlines(self):
        # given
        history = textwrap.dedent(f"""
        \n
            /home/user/documents\n
            /home/user/downloads
            /home/user/foo
            /home/user/bar
            \n
        """)
        self.create_test_file(history)
        max_lines = -1
        reader = self.create_reader(max_lines)

        # when
        reader.read()

        # then
        expected_calls = [
            call('/home/user/bar'),
            call('/home/user/foo'),
            call('/home/user/downloads'),
            call('/home/user/documents'),
        ]
        self.mock_callback.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(4, self.mock_callback.call_count)

    def test_emtpy_dirs_file(self):
        # given
        history = ""
        self.create_test_file(history)
        max_lines = -1
        reader = self.create_reader(max_lines)

        # when
        reader.read()

        # then
        self.mock_callback.assert_not_called()

    def test_only_whitespace_dirs_file(self):
        # given
        history = " \n  "
        self.create_test_file(history)
        max_lines = -1
        reader = self.create_reader(max_lines)

        # when
        reader.read()

        # then
        self.mock_callback.assert_not_called()


if __name__ == '__main__':
    unittest.main()
