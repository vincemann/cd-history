import unittest
from unittest.mock import patch

from cd_history.mode import Mode
from cd_history.mode_parser import eval_mode


class TestEvalMode(unittest.TestCase):

    @patch('sys.argv', ['cd-history'])
    def test_default_mode_no_args(self):
        self.assertEqual(eval_mode(), Mode.DEFAULT)

    @patch('sys.argv', ['cd-history', '--mode=terminal'])
    def test_default_mode_with_arg(self):
        self.assertEqual(eval_mode(), Mode.DEFAULT)

    @patch('sys.argv', ['cd-history', '--action=select', '--mode=gui'])
    def test_default_mode_with_args(self):
        self.assertEqual(eval_mode(), Mode.DEFAULT)

    @patch('sys.argv', ['cd-history', '-h'])
    def test_default_mode_with_help(self):
        self.assertEqual(eval_mode(), Mode.DEFAULT)

    @patch('sys.argv', ['cd-history', 'clean'])
    def test_clean_mode(self):
        self.assertEqual(eval_mode(), Mode.CLEAN)

    @patch('sys.argv', ['cd-history', 'append'])
    def test_append_mode(self):
        self.assertEqual(eval_mode(), Mode.APPEND)

    @patch('sys.argv', ['cd-history', 'invalid'])
    def test_invalid_mode(self):
        self.assertIsNone(eval_mode())


if __name__ == '__main__':
    unittest.main()
