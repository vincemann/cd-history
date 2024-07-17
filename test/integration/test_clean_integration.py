import os
import sys
import textwrap
import unittest
from unittest.mock import patch

from cd_history.args import HISTORY_FILE_ENV, SCRIPT_NAME
from cd_history.clean.clean_app import CleanApp
from test.integration.suite.utils import resolve_test_file_path


class TestCleanIntegration(unittest.TestCase):

    def setUp(self):
        self.cd_history_path = resolve_test_file_path("cd_history")
        self.default_env = os.environ.copy()

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

    def read_cd_history(self):
        with open(self.cd_history_path, 'r') as f:
            return f.read().splitlines()

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_clean_script_remove_rel_paths(self, mock_isdir):
        # given
        cd_history = textwrap.dedent("""
        /home/user/valid_dir1
        relative/path1
        /home/user/valid_dir2
        another/relative/path2
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
        cli_args = [
            SCRIPT_NAME,
            "clean",
        ]
        sys.argv = cli_args
        CleanApp().start()

        # then
        expected_content = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3"
        ]
        actual_content = self.read_cd_history()
        self.assertEqual(expected_content, actual_content)

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_clean_script_remove_duplicate(self, mock_isdir):
        # given
        cd_history = textwrap.dedent("""
        /home/user/valid_dir1
        /home/user/valid_dir2
        /home/user/valid_dir3
        /home/user/valid_dir2\n
        """).strip()

        existing_dirs = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3",
        ]

        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)
        self.setup_cd_history(cd_history)

        # when
        cli_args = [
            SCRIPT_NAME,
            "clean",
        ]
        sys.argv = cli_args
        CleanApp().start()

        # then
        expected_content = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir3",
            "/home/user/valid_dir2",
        ]
        actual_content = self.read_cd_history()
        self.assertEqual(expected_content, actual_content)

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_clean_script_empty_file(self, mock_isdir):
        # given
        cd_history = ""

        existing_dirs = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3",
        ]

        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)
        self.setup_cd_history(cd_history)

        # when
        cli_args = [
            SCRIPT_NAME,
            "clean",
        ]
        sys.argv = cli_args
        CleanApp().start()

        # then
        expected_content = []
        actual_content = self.read_cd_history()
        self.assertEqual(expected_content, actual_content)

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_clean_script_newline_file(self, mock_isdir):
        # given
        cd_history = "\n"

        existing_dirs = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3",
        ]

        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)
        self.setup_cd_history(cd_history)

        # when
        cli_args = [
            SCRIPT_NAME,
            "clean",
        ]
        sys.argv = cli_args
        CleanApp().start()

        # then
        expected_content = []
        actual_content = self.read_cd_history()
        self.assertEqual(expected_content, actual_content)

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_clean_script_all_valid(self, mock_isdir):
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
        ]

        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)
        self.setup_cd_history(cd_history)

        # when
        cli_args = [
            SCRIPT_NAME,
            "clean",
        ]
        sys.argv = cli_args
        CleanApp().start()

        # then
        expected_content = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3"
        ]
        actual_content = self.read_cd_history()
        self.assertEqual(expected_content, actual_content)

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_clean_script_all_valid_with_whitespaces(self, mock_isdir):
        # given
        cd_history = textwrap.dedent("""
        /home/user/valid_dir1
        /home/user/valid dir2
        /home/user/valid_dir3
        """).strip()

        existing_dirs = [
            "/home/user/valid_dir1",
            "/home/user/valid dir2",
            "/home/user/valid_dir3",
        ]

        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)
        self.setup_cd_history(cd_history)

        # when
        cli_args = [
            SCRIPT_NAME,
            "clean",
        ]
        sys.argv = cli_args
        CleanApp().start()

        # then
        expected_content = [
            "/home/user/valid_dir1",
            "/home/user/valid dir2",
            "/home/user/valid_dir3"
        ]
        actual_content = self.read_cd_history()
        self.assertEqual(expected_content, actual_content)

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_clean_script_all_valid_multiple_iterations(self, mock_isdir):
        def assert_stayed_same():
            # then
            expected_content = [
                "/home/user/valid_dir1",
                "/home/user/valid_dir2",
                "/home/user/valid_dir3"
            ]
            actual_content = self.read_cd_history()
            self.assertEqual(expected_content, actual_content)
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
        ]

        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)
        self.setup_cd_history(cd_history)

        # when
        cli_args = [
            SCRIPT_NAME,
            "clean",
        ]
        sys.argv = cli_args
        for i in range(20):
            CleanApp().start()
            assert_stayed_same()

        assert_stayed_same()

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_clean_script_fixes_then_stays_same_multiple_iterations(self, mock_isdir):
        def assert_correct_state():
            # then
            expected_content = [
                "/home/user/valid_dir1",
                "/home/user/valid_dir2",
                "/home/user/valid_dir3",
            ]
            actual_content = self.read_cd_history()
            self.assertEqual(expected_content, actual_content)
        # given
        cd_history = textwrap.dedent("""
        /home/user/valid_dir1
        /some/unexisting
        /home/user/valid_dir2
        invalid/dir
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
        cli_args = [
            SCRIPT_NAME,
            "clean",
        ]
        sys.argv = cli_args
        for i in range(20):
            CleanApp().start()
            assert_correct_state()

        assert_correct_state()

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_clean_script_remove_non_existent_dirs(self, mock_isdir):
        # given
        cd_history = textwrap.dedent("""
        /home/user/valid_dir1
        /home/user/valid_dir2
        /home/user/valid_dir3
        """).strip()

        existing_dirs = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir3",
        ]

        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)
        self.setup_cd_history(cd_history)

        # when
        cli_args = [
            SCRIPT_NAME,
            "clean",
        ]
        sys.argv = cli_args
        CleanApp().start()

        # then
        expected_content = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir3"
        ]
        actual_content = self.read_cd_history()
        self.assertEqual(expected_content, actual_content)


if __name__ == '__main__':
    unittest.main()
