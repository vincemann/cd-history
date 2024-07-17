import os
import textwrap
import unittest
from unittest.mock import patch

from cd_history.clean.cd_history_cleaner import CdHistoryCleaner


class TestCdHistoryCleaner(unittest.TestCase):

    # give me file name of file in test/integration and this function resolves it to abs path
    def resolve_test_file_path(self, filename):
        return os.path.join(os.path.dirname(__file__), filename)

    def setUp(self):
        self.file_path = self.resolve_test_file_path("test-cd-history")

    def existing_dirs(self, mock_is_dir, dirs):
        mock_is_dir.side_effect = lambda dir: dir in dirs


    def write_to_test_file(self, content):
        with open(self.file_path, 'w') as f:
            f.write(content)

    def read_from_test_file(self):
        with open(self.file_path, 'r') as f:
            return f.read().splitlines()

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_clean_removes_non_existing_dirs(self, mock_isdir):
        # given
        content = textwrap.dedent("""
        /home/user/valid_dir1
        /home/user/invalid_dir
        /home/user/valid_dir2
        """).strip()
        self.existing_dirs(mock_isdir, [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
        ])
        self.write_to_test_file(content)
        cleaner = CdHistoryCleaner(self.file_path)

        # when
        cleaner.clean()

        # then
        # most recent stuff is at the end of file
        expected_content = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
        ]
        actual_content = self.read_from_test_file()
        self.assertEqual(expected_content, actual_content)
        self.assert_file_ends_with_newline()

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_clean_removes_only_non_existing_dirs(self, mock_isdir):
        content = textwrap.dedent("""
        /home/user/invalid_dir1
        /home/user/invalid_dir2
        """).strip()
        self.existing_dirs(mock_isdir, [])
        self.write_to_test_file(content)
        cleaner = CdHistoryCleaner(self.file_path)

        cleaner.clean()

        expected_content = []
        actual_content = self.read_from_test_file()
        self.assertEqual(expected_content, actual_content)

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_clean_removes_duplicates(self, mock_isdir):
        content = textwrap.dedent("""
        /home/user/valid_dir1
        /home/user/valid_dir1
        /home/user/valid_dir2
        /home/user/valid_dir2
        """).strip()
        self.existing_dirs(mock_isdir, [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
        ])
        self.write_to_test_file(content)
        cleaner = CdHistoryCleaner(self.file_path)

        cleaner.clean()

        expected_content = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2"
        ]
        actual_content = self.read_from_test_file()
        self.assertEqual(expected_content, actual_content)
        self.assert_file_ends_with_newline()

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_clean_removes_multiple_duplicates(self, mock_isdir):
        content = textwrap.dedent("""
        /home/user/valid_dir1
        /home/user/valid_dir1
        /home/user/valid_dir1
        /home/user/valid_dir2
        /home/user/valid_dir1
        /home/user/valid_dir2
        """).strip()
        self.existing_dirs(mock_isdir, [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
        ])
        self.write_to_test_file(content)
        cleaner = CdHistoryCleaner(self.file_path)

        cleaner.clean()

        expected_content = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2"
        ]
        actual_content = self.read_from_test_file()
        self.assertEqual(expected_content, actual_content)
        self.assert_file_ends_with_newline()

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_clean_removes_duplicates_preserve_order(self, mock_isdir):
        content = textwrap.dedent("""
        /home/user/valid_dir3
        /home/user/valid_dir1
        /home/user/valid_dir2
        /home/user/valid_dir1
        """).strip()
        self.existing_dirs(mock_isdir, [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3",
        ])
        self.write_to_test_file(content)
        cleaner = CdHistoryCleaner(self.file_path)

        cleaner.clean()

        expected_content = [
            "/home/user/valid_dir3",
            "/home/user/valid_dir2",
            "/home/user/valid_dir1"
        ]
        actual_content = self.read_from_test_file()
        self.assertEqual(expected_content, actual_content)
        self.assert_file_ends_with_newline()

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_clean_handles_empty_file(self, mock_isdir):
        content = ""
        self.existing_dirs(mock_isdir, [])
        self.write_to_test_file(content)
        cleaner = CdHistoryCleaner(self.file_path)

        cleaner.clean()

        expected_content = []
        actual_content = self.read_from_test_file()
        self.assertEqual(expected_content, actual_content)

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_clean_handles_mixed_content(self, mock_isdir):
        content = textwrap.dedent("""
        /home/user/valid_dir1
        /home/user/invalid_dir
        /home/user/valid_dir2
        /home/user/valid_dir1
        /home/user/invalid_dir2
        /home/user/valid_dir2
        """).strip()
        self.existing_dirs(mock_isdir, [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
        ])
        self.write_to_test_file(content)
        cleaner = CdHistoryCleaner(self.file_path)

        cleaner.clean()

        expected_content = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2"
        ]
        actual_content = self.read_from_test_file()
        self.assertEqual(expected_content, actual_content)
        self.assert_file_ends_with_newline()

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_clean_no_modifications_needed(self, mock_isdir):
        content = textwrap.dedent("""
        /home/user/valid_dir1
        /home/user/valid_dir2
        /home/user/valid_dir3
        """).strip()
        self.existing_dirs(mock_isdir, [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3"
        ])
        self.write_to_test_file(content)
        cleaner = CdHistoryCleaner(self.file_path)

        cleaner.clean()

        expected_content = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3"
        ]
        actual_content = self.read_from_test_file()
        self.assertEqual(expected_content, actual_content)
        self.assert_file_ends_with_newline()

    def test_clean_multiple_times_no_modifications_needed(self):
        self.test_clean_no_modifications_needed()
        self.test_clean_no_modifications_needed()
        self.test_clean_no_modifications_needed()

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_clean_discard_relative_dirs(self, mock_isdir):
        content = textwrap.dedent("""
        /home/user/valid_dir1
        relative/path1
        /home/user/valid_dir2
        another/relative/path2
        /home/user/valid_dir3
        """).strip()
        self.existing_dirs(mock_isdir, [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3"
        ])
        self.write_to_test_file(content)
        cleaner = CdHistoryCleaner(self.file_path)

        cleaner.clean()

        expected_content = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3"
        ]
        actual_content = self.read_from_test_file()
        self.assertEqual(expected_content, actual_content)
        self.assert_file_ends_with_newline()

    @patch('cd_history.file_checker.FileChecker.isdir')
    def test_clean_discard_newlines_between_dirs(self, mock_isdir):
        content = textwrap.dedent("""
        /home/user/valid_dir1
        
        /home/user/valid_dir2
        
        /home/user/valid_dir3
        """).strip()
        self.existing_dirs(mock_isdir, [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3"
        ])
        self.write_to_test_file(content)
        cleaner = CdHistoryCleaner(self.file_path)

        cleaner.clean()

        expected_content = [
            "/home/user/valid_dir1",
            "/home/user/valid_dir2",
            "/home/user/valid_dir3"
        ]
        actual_content = self.read_from_test_file()
        self.assertEqual(expected_content, actual_content)
        self.assert_file_ends_with_newline()

    def assert_file_ends_with_newline(self):
        with open(self.file_path, 'rb') as file:
            file.seek(-1, 2)  # Move the cursor to the last byte in the file
            last_char = file.read(1)
            self.assertTrue(last_char == b'\n')


if __name__ == '__main__':
    unittest.main()
