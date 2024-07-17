import unittest
from unittest.mock import MagicMock, patch

from cd_history.dir_filter import DirFilter


class TestDirFilter(unittest.TestCase):

    def setUp(self):
        self.mock_file_checker = MagicMock()
        patch('cd_history.dir_filter.FileChecker', return_value=self.mock_file_checker).start()
        self.addCleanup(patch.stopall)

    def test_accept_abs_path(self):
        # given
        dir_filter = DirFilter("")
        self.mock_file_checker.isdir.return_value = True

        # when
        result = dir_filter.accept("/home/user/documents")

        # then
        self.assertTrue(result)
        self.mock_file_checker.isdir.assert_called_with("/home/user/documents")

    def test_reject_non_abs_path(self):
        # given
        dir_filter = DirFilter("")

        # when
        result = dir_filter.accept("relative/path")

        # then
        self.assertFalse(result)

    def test_reject_non_existing_dir(self):
        # given
        dir_filter = DirFilter("")
        self.mock_file_checker.isdir.return_value = False

        # when
        result = dir_filter.accept("/home/user/nonexisting")

        # then
        self.assertFalse(result)

    def test_reject_duplicate_dir(self):
        # given
        dir_filter = DirFilter("")
        self.mock_file_checker.isdir.return_value = True

        # when
        result1 = dir_filter.accept("/home/user/documents")
        result2 = dir_filter.accept("/home/user/documents")

        # then
        self.assertTrue(result1)
        self.assertFalse(result2)

    def test_filter_dirs(self):
        # given
        filter_pattern = "foo|bar"
        dir_filter = DirFilter(filter_pattern)
        self.mock_file_checker.isdir.return_value = True

        # when
        result1 = dir_filter.accept("/home/user/foo")
        result2 = dir_filter.accept("/home/user/bar")
        result3 = dir_filter.accept("/home/user/other")

        # then
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertFalse(result3)


if __name__ == '__main__':
    unittest.main()
