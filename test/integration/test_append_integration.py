import io
import os
import sys
import textwrap
import unittest
from unittest.mock import patch

from cd_history.append.append_app import AppendApp, USAGE_STRING
from cd_history.args import HISTORY_FILE_ENV, SCRIPT_NAME
from cd_history.error_msgs import NON_EXISTENT_DIR_MSG, NO_ABS_PATH_DIR_MSG
from test.integration.suite.utils import resolve_test_file_path, assert_printed_to_stream


class TestAppendIntegration(unittest.TestCase):

    def setUp(self):
        self.cd_history_path = resolve_test_file_path("cd_history")
        self.default_env = os.environ.copy()
        self.stdout_buf = io.StringIO()

    def assert_printed_to_stdout(self, expected_outputs, strict=True):
        return assert_printed_to_stream(self.stdout_buf, expected_outputs, strict=strict)

    def tearDown(self):
        os.environ = self.default_env

    def create_dir_checker_mock(self, existing_dirs):
        def mock_isdir(path):
            return path in existing_dirs

        return mock_isdir

    def setup_cd_history(self, content):
        path = self.cd_history_path
        with open(path, 'w') as f:
            f.write(content)
        os.environ[HISTORY_FILE_ENV] = path
        return path

    def start(self, dir):
        original_stdout = sys.stdout
        try:
            if dir:
                cli_args = [
                    SCRIPT_NAME,
                    "append",
                    dir,
                ]
            else:
                cli_args = [
                    SCRIPT_NAME,
                    "append",
                ]
            sys.argv = cli_args
            sys.stdout = self.stdout_buf
            AppendApp().start()
        finally:
            sys.stdout = original_stdout

    def read_cd_history(self):
        with open(self.cd_history_path, 'r') as f:
            return f.read().splitlines()

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_append_dir(self, mock_isdir):
        # given
        dir_to_append = "/home/user/valid_dir4"
        cd_history = textwrap.dedent("""
        /home/user/valid_dir1
        /home/user/valid_dir2
        /home/user/valid_dir3\n
        """).strip()

        existing_dirs = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3",
            dir_to_append,
        ]

        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)
        self.setup_cd_history(cd_history)

        # when
        self.start(dir_to_append)

        # then
        expected_content = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3",
            dir_to_append,
        ]
        actual_content = self.read_cd_history()
        self.assertEqual(expected_content, actual_content)

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_append_dir_with_whitespaces(self, mock_isdir):
        # given
        dir_to_append = "/home/user/valid dir4"
        cd_history = textwrap.dedent("""
        /home/user/valid_dir1
        /home/user/valid_dir2
        /home/user/valid_dir3\n
        """).strip()

        existing_dirs = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3",
            dir_to_append,
        ]

        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)
        self.setup_cd_history(cd_history)

        # when
        self.start(dir_to_append)

        # then
        expected_content = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3",
            dir_to_append,
        ]
        actual_content = self.read_cd_history()
        self.assertEqual(expected_content, actual_content)

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_append_already_existing_dir(self, mock_isdir):
        # given
        dir_to_append = "/home/user/valid_dir2"
        cd_history = textwrap.dedent("""
        /home/user/valid_dir1
        /home/user/valid_dir2
        /home/user/valid_dir3\n
        """).strip()

        existing_dirs = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3",
            dir_to_append,
        ]

        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)
        self.setup_cd_history(cd_history)

        # when
        self.start(dir_to_append)

        # then
        expected_content = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3",
            dir_to_append,
        ]
        actual_content = self.read_cd_history()
        self.assertEqual(expected_content, actual_content)

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_append_dir_to_empty_file(self, mock_isdir):
        # given
        dir_to_append = "/home/user/valid_dir4"
        cd_history = textwrap.dedent("""
        """).strip()

        existing_dirs = [
            dir_to_append,
        ]

        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)
        self.setup_cd_history(cd_history)

        # when
        self.start(dir_to_append)

        # then
        expected_content = [
            dir_to_append,
        ]
        actual_content = self.read_cd_history()
        self.assertEqual(expected_content, actual_content)

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_append_dir_to_newline_only_file(self, mock_isdir):
        # given
        dir_to_append = "/home/user/valid_dir4"
        cd_history = textwrap.dedent("""\n
        """).strip()

        existing_dirs = [
            dir_to_append,
        ]

        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)
        self.setup_cd_history(cd_history)

        # when
        self.start(dir_to_append)

        # then
        expected_content = [
            dir_to_append,
        ]
        actual_content = self.read_cd_history()
        self.assertEqual(expected_content, actual_content)

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_append_dir_no_end_newline(self, mock_isdir):
        # given
        dir_to_append = "/home/user/valid_dir4"
        cd_history = textwrap.dedent("""
        /home/user/valid_dir1
        /home/user/valid_dir2
        /home/user/valid_dir3
        """).strip()

        existing_dirs = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3",
            dir_to_append,
        ]

        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)
        self.setup_cd_history(cd_history)

        # when
        self.start(dir_to_append)

        # then
        expected_content = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3",
            dir_to_append,
        ]
        actual_content = self.read_cd_history()
        self.assertEqual(expected_content, actual_content)

    @patch('cd_history.append.append_app.AppendApp.exit')
    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_append_non_existing_dir(self, mock_isdir, mock_exit):
        # given
        dir_to_append = "/home/user/valid_dir4"
        cd_history = textwrap.dedent("""
        /home/user/valid_dir1
        /home/user/valid_dir2
        /home/user/valid_dir3
        """).strip()

        existing_dirs = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3",
        ]

        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)
        self.setup_cd_history(cd_history)

        # when
        self.start(dir_to_append)

        # then
        expected_content = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3",
        ]
        actual_content = self.read_cd_history()
        self.assertEqual(expected_content, actual_content)
        mock_exit.assert_called_once_with(1)
        self.assert_printed_to_stdout([NON_EXISTENT_DIR_MSG(dir_to_append)])

    @patch('cd_history.append.append_app.AppendApp.exit')
    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_append_invalid_dir(self, mock_isdir, mock_exit):
        # given
        dir_to_append = "user/valid_dir4"
        cd_history = textwrap.dedent("""
        /home/user/valid_dir1
        /home/user/valid_dir2
        /home/user/valid_dir3
        """).strip()

        existing_dirs = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3",
            "/home/user/valid_dir4",
        ]

        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)
        self.setup_cd_history(cd_history)

        # when
        self.start(dir_to_append)

        # then
        expected_content = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3",
        ]
        actual_content = self.read_cd_history()
        self.assertEqual(expected_content, actual_content)
        mock_exit.assert_called_once_with(1)
        self.assert_printed_to_stdout([NO_ABS_PATH_DIR_MSG(dir_to_append)])

    @patch('cd_history.append.append_app.AppendApp.exit')
    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_dir_arg_missing(self, mock_isdir, mock_exit):
        # given
        cd_history = textwrap.dedent("""
        /home/user/valid_dir1
        /home/user/valid_dir2
        /home/user/valid_dir3
        """).strip()

        existing_dirs = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3",
            "/home/user/valid_dir4",
        ]

        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)
        self.setup_cd_history(cd_history)

        # when
        self.start(dir=None)

        # then
        expected_content = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3",
        ]
        actual_content = self.read_cd_history()
        self.assertEqual(expected_content, actual_content)
        mock_exit.assert_called_once_with(1)
        self.assert_printed_to_stdout(["Invalid amount of args, " + USAGE_STRING])


if __name__ == '__main__':
    unittest.main()
