import os
import sys
import textwrap
import time
import unittest
from unittest.mock import patch
from cd_history.error_msgs import *

from cd_history.args import *
from test.integration.suite.app_interactor import AppInteractor
from test.integration.suite.delayed_input import DelayedInput
from test.integration.suite.app_test_executor import TestExecutor
from test.integration.suite.utils import resolve_test_file_path


class IntegrationTest(unittest.TestCase):

    def remove_if_exists(self, filepath):
        if os.path.exists(filepath):
            os.remove(filepath)

    def setUp(self):
        self.default_env = os.environ.copy()
        self.app = AppInteractor()
        self.executor = TestExecutor(self.app)

    def create_file_checker_mock(self, existing_files):
        def mock_isfile(path):
            return path in existing_files

        return mock_isfile

    def create_dir_checker_mock(self, existing_dirs):
        def mock_isdir(path):
            return path in existing_dirs

        return mock_isdir

    def setup_cd_history(self, content):
        path = resolve_test_file_path("cd_history")
        with open(path, 'w') as f:
            f.write(content)
        os.environ[HISTORY_FILE_ENV] = path
        return path

    @patch('cd_history.file_checker.FileChecker.isdir')
    @patch('cd_history.file_checker.FileChecker.isfile')
    def test_select_dir_in_terminal(self, mock_isfile, mock_isdir):
        # given
        cd_history = textwrap.dedent(f"""
            /home/user/Downloads
            /home/user/dessen
            /home/user/doc
        """).strip()

        cd_history_file = self.setup_cd_history(cd_history)

        existing_files = [
            cd_history_file,
        ]
        existing_dirs = [
            "/home/user/Downloads",
            "/home/user/dessen",
            "/home/user/doc",
        ]

        mock_isfile.side_effect = self.create_file_checker_mock(existing_files)
        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)

        # using default action
        cli_args = [
            SCRIPT_NAME,
            MODE_ARG, "terminal",
        ]
        sys.argv = cli_args
        delayed_input = DelayedInput()

        def test():
            self.app.wait_until_search_done()
            expected_outputs = [
                "1: /home/user/doc",
                "2: /home/user/dessen",
                "3: /home/user/Downloads",
            ]
            self.app.assert_printed_to_stderr(expected_outputs)

            # now give it the input -> selecting file 3
            delayed_input.release_input("3\n")
            # then
            self.app.wait_until_app_finished()
            self.app.print_stderr()
            self.app.print_stdout()
            self.app.assert_app_finished_with_result(successful=True)
            expected_selection = "/home/user/Downloads"
            self.app.assert_printed_to_stdout([expected_selection], strict=True)

        self.executor.start_test_in_process(test, delayed_input)

    @patch('cd_history.file_checker.FileChecker.isdir')
    @patch('cd_history.file_checker.FileChecker.isfile')
    def test_select_filtered_dir_in_terminal(self, mock_isfile, mock_isdir):
        # given
        cd_history = textwrap.dedent(f"""
            /home/user/Downloads
            /home/user/dessen
            /home/user/sshgil
            /home/user/doc
            /home/ssh/doc
        """).strip()

        cd_history_file = self.setup_cd_history(cd_history)

        existing_files = [
            cd_history_file,
        ]
        existing_dirs = [
            "/home/user/Downloads",
            "/home/user/dessen",
            "/home/user/doc",
            "/home/ssh/doc",
            "/home/user/sshgil"
        ]

        mock_isfile.side_effect = self.create_file_checker_mock(existing_files)
        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)

        filter = "ssh"
        # using default action
        cli_args = [
            SCRIPT_NAME,
            MODE_ARG, "terminal",
            FILTER_ARG, filter
        ]
        sys.argv = cli_args
        delayed_input = DelayedInput()

        def test():
            self.app.wait_until_search_done()
            expected_outputs = [
                "1: /home/ssh/doc",
                "2: /home/user/sshgil",
            ]
            self.app.assert_printed_to_stderr(expected_outputs)

            # now give it the input -> selecting file 3
            delayed_input.release_input("2\n")
            # then
            self.app.wait_until_app_finished()
            self.app.print_stderr()
            self.app.assert_app_finished_with_result(successful=True)
            expected_selection = "/home/user/sshgil"
            self.app.assert_printed_to_stdout([expected_selection], strict=True)

        self.executor.start_test_in_process(test, delayed_input)

    @patch('cd_history.file_checker.FileChecker.isdir')
    @patch('cd_history.file_checker.FileChecker.isfile')
    def test_select_popup_filtered_dir_in_terminal(self, mock_isfile, mock_isdir):
        # given
        cd_history = textwrap.dedent(f"""
            /home/user/Downloads
            /home/user/dessen
            /home/user/sshgil
            /home/user/doc
            /home/ssh/doc
        """).strip()

        cd_history_file = self.setup_cd_history(cd_history)

        existing_files = [
            cd_history_file,
        ]
        existing_dirs = [
            "/home/user/Downloads",
            "/home/user/dessen",
            "/home/user/doc",
            "/home/ssh/doc",
            "/home/user/sshgil"
        ]

        mock_isfile.side_effect = self.create_file_checker_mock(existing_files)
        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)

        cli_args = [
            SCRIPT_NAME,
            MODE_ARG, "terminal",
            FILTER_ARG, "popup"
        ]
        sys.argv = cli_args
        delayed_input = DelayedInput()

        def test():
            self.app.wait_until_app_set()
            delayed_input.release_input("ssh\n")
            self.app.wait_until_search_done()
            expected_outputs = [
                "Enter Filter:",
                "1: /home/ssh/doc",
                "2: /home/user/sshgil",
            ]
            self.app.assert_printed_to_stderr(expected_outputs)

            # now give it the input -> selecting file 3
            delayed_input.release_input("2\n")
            # then
            self.app.wait_until_app_finished()
            self.app.print_stderr()
            self.app.assert_app_finished_with_result(successful=True)
            expected_selection = "/home/user/sshgil"
            self.app.assert_printed_to_stdout([expected_selection], strict=True)

        self.executor.start_test_in_process(test, delayed_input)

    @patch('cd_history.app_launcher.DefaultAppLauncher.exit')
    def test_missing_cd_history_env_var_in_terminal(self, mock_exit):
        # given
        if HISTORY_FILE_ENV in os.environ:
            del os.environ[HISTORY_FILE_ENV]

        cli_args = [
            SCRIPT_NAME,
            MODE_ARG, "terminal",
        ]
        sys.argv = cli_args
        self.app.set_raise_exceptions(False)

        def test():
            self.app.wait_until_app_finished()
            mock_exit.assert_called_once_with(1)
            self.app.print_stderr()
            self.app.assert_printed_to_stderr([MISSING_CD_HISTORY_ENV_VAR_MSG])

        self.executor.start_test_in_process(test)

    def test_non_existent_cd_history_file_in_terminal_gets_generated_with_warning(self):
        # given
        cd_history_path = "/tmp/nonexistent"
        self.remove_if_exists(cd_history_path)
        os.environ[HISTORY_FILE_ENV] = cd_history_path

        cli_args = [
            SCRIPT_NAME,
            MODE_ARG, "terminal",
        ]
        sys.argv = cli_args

        def test():
            self.app.wait_until_app_finished()
            self.app.assert_app_finished_with_result(successful=True)
            self.app.print_stderr()
            err_msg = CD_HISTORY_FILE_NOT_FOUND_MSG(cd_history_path)
            self.app.assert_printed_to_stderr([err_msg], strict=True)
            # file was generated
            self.assertTrue(os.path.exists(cd_history_path))

        self.executor.start_test_in_process(test)

    @patch('cd_history.file_checker.FileChecker.isdir')
    @patch('cd_history.file_checker.FileChecker.isfile')
    def test_exit_after_search_in_terminal(self, mock_isfile, mock_isdir):
        # given
        cd_history = textwrap.dedent(f"""
            /home/user/Downloads
            /home/user/dessen
            /home/user/doc
        """).strip()

        cd_history_file = self.setup_cd_history(cd_history)

        existing_files = [
            cd_history_file,
        ]
        existing_dirs = [
            "/home/user/Downloads",
            "/home/user/dessen",
            "/home/user/doc",
        ]

        mock_isfile.side_effect = self.create_file_checker_mock(existing_files)
        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)

        # using default action
        cli_args = [
            SCRIPT_NAME,
            MODE_ARG, "terminal",
        ]
        sys.argv = cli_args
        delayed_input = DelayedInput()

        def test():
            self.app.wait_until_search_done()
            expected_outputs = [
                "1: /home/user/doc",
                "2: /home/user/dessen",
                "3: /home/user/Downloads",
            ]
            self.app.assert_printed_to_stderr(expected_outputs)

            # exit
            delayed_input.release_input("\n")
            # then
            self.app.wait_until_app_finished()
            self.app.print_stderr()
            self.app.assert_app_finished_with_result(successful=True)
            self.app.print_stdout()
            self.app.assert_nothing_printed_to_stdout()

        self.executor.start_test_in_process(test, delayed_input)

    @patch('cd_history.file_checker.FileChecker.isdir')
    @patch('cd_history.file_checker.FileChecker.isfile')
    def test_select_dir_in_gui(self, mock_isfile, mock_isdir):
        # given
        cd_history = textwrap.dedent(f"""
            /home/user/Downloads
            /home/user/dessen
            /home/user/doc
        """).strip()

        cd_history_file = self.setup_cd_history(cd_history)

        existing_files = [
            cd_history_file,
        ]
        existing_dirs = [
            "/home/user/Downloads",
            "/home/user/dessen",
            "/home/user/doc",
        ]

        mock_isfile.side_effect = self.create_file_checker_mock(existing_files)
        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)

        # using default action
        cli_args = [
            SCRIPT_NAME,
            MODE_ARG, "gui",
        ]
        sys.argv = cli_args

        def test():
            self.app.wait_until_search_done()
            self.app.wait_until_window_open()
            expected_outputs = [
                "/home/user/doc",
                "/home/user/dessen",
                "/home/user/Downloads",
            ]
            self.app.assert_dirs_displayed(expected_outputs)

            # selecting file 2
            self.app.press_down()
            self.app.press_down()
            self.app.press_enter()
            # then
            self.app.wait_until_app_finished()
            self.app.print_stderr()
            self.app.assert_app_finished_with_result(successful=True)
            expected_selection = "/home/user/Downloads"
            self.app.assert_printed_to_stdout([expected_selection], strict=True)

        self.executor.start_test_in_process(test)

    @patch('cd_history.file_checker.FileChecker.isdir')
    @patch('cd_history.file_checker.FileChecker.isfile')
    def test_select_filtered_dir_in_gui(self, mock_isfile, mock_isdir):
        # given
        cd_history = textwrap.dedent(f"""
            /home/user/Downloads
            /home/user/dessen
            /home/user/sshgil
            /home/user/doc
            /home/ssh/doc
        """).strip()

        cd_history_file = self.setup_cd_history(cd_history)

        existing_files = [
            cd_history_file,
        ]
        existing_dirs = [
            "/home/user/Downloads",
            "/home/user/dessen",
            "/home/user/sshgil",
            "/home/user/doc",
            "/home/ssh/doc",
        ]

        mock_isfile.side_effect = self.create_file_checker_mock(existing_files)
        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)

        # using default action
        filter = "ssh"
        cli_args = [
            SCRIPT_NAME,
            MODE_ARG, "gui",
            FILTER_ARG, filter
        ]
        sys.argv = cli_args

        def test():
            self.app.wait_until_search_done()
            self.app.wait_until_window_open()
            expected_outputs = [
                "/home/ssh/doc",
                "/home/user/sshgil",
            ]
            self.app.assert_dirs_displayed(expected_outputs)

            # selecting file 2
            self.app.press_down()
            self.app.press_enter()
            # then
            self.app.wait_until_app_finished()
            self.app.print_stderr()
            self.app.assert_app_finished_with_result(successful=True)
            expected_selection = "/home/user/sshgil"
            self.app.assert_printed_to_stdout([expected_selection], strict=True)

        self.executor.start_test_in_process(test)

    @patch('cd_history.gui.gui_popup.GuiPopup.ask_for_filter')
    @patch('cd_history.file_checker.FileChecker.isdir')
    @patch('cd_history.file_checker.FileChecker.isfile')
    def test_select_popup_filtered_dir_in_gui(self, mock_isfile, mock_isdir, popup_filter_mock):
        # given
        cd_history = textwrap.dedent(f"""
            /home/user/Downloads
            /home/user/dessen
            /home/user/sshgil
            /home/user/doc
            /home/ssh/doc
        """).strip()

        cd_history_file = self.setup_cd_history(cd_history)

        existing_files = [
            cd_history_file,
        ]
        existing_dirs = [
            "/home/user/Downloads",
            "/home/user/dessen",
            "/home/user/sshgil",
            "/home/user/doc",
            "/home/ssh/doc",
        ]

        mock_isfile.side_effect = self.create_file_checker_mock(existing_files)
        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)

        # using default action
        cli_args = [
            SCRIPT_NAME,
            MODE_ARG, "gui",
            FILTER_ARG, "popup"
        ]
        sys.argv = cli_args
        popup_filter_mock.return_value = "ssh"

        def test():
            self.app.wait_until_search_done()
            self.app.wait_until_window_open()
            expected_outputs = [
                "/home/ssh/doc",
                "/home/user/sshgil",
            ]
            self.app.assert_dirs_displayed(expected_outputs)

            # selecting file 2
            self.app.press_down()
            self.app.press_enter()
            # then
            self.app.wait_until_app_finished()
            self.app.print_stderr()
            self.app.assert_app_finished_with_result(successful=True)
            expected_selection = "/home/user/sshgil"
            self.app.assert_printed_to_stdout([expected_selection], strict=True)

        self.executor.start_test_in_process(test)

    @patch('cd_history.file_checker.FileChecker.isdir')
    @patch('cd_history.file_checker.FileChecker.isfile')
    def test_exit_after_search_in_gui(self, mock_isfile, mock_isdir):
        # given
        cd_history = textwrap.dedent(f"""
            /home/user/Downloads
            /home/user/dessen
            /home/user/doc
        """).strip()

        cd_history_file = self.setup_cd_history(cd_history)

        existing_files = [
            cd_history_file,
        ]
        existing_dirs = [
            "/home/user/Downloads",
            "/home/user/dessen",
            "/home/user/doc",
        ]

        mock_isfile.side_effect = self.create_file_checker_mock(existing_files)
        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)

        # using default action
        cli_args = [
            SCRIPT_NAME,
            MODE_ARG, "gui",
        ]
        sys.argv = cli_args

        def test():
            self.app.wait_until_search_done()
            self.app.wait_until_window_open()
            expected_outputs = [
                "/home/user/doc",
                "/home/user/dessen",
                "/home/user/Downloads",
            ]
            self.app.assert_dirs_displayed(expected_outputs)

            # exit
            self.app.press_escape()
            # then
            self.app.wait_until_app_finished()
            self.app.print_stderr()
            self.app.assert_app_finished_with_result(successful=True)
            self.app.assert_nothing_printed_to_stdout()
        self.executor.start_test_in_process(test)

    @patch('cd_history.file_checker.FileChecker.isdir')
    @patch('cd_history.file_checker.FileChecker.isfile')
    def test_select_dir_while_search_running_in_gui(self, mock_isfile, mock_isdir):
        # given
        cd_history = textwrap.dedent(f"""
            /home/user/Downloads
            /home/user/dessen
            /home/user/doc
            /home/user/doc1
            /home/user/doc2
            /home/user/doc3
        """).strip()

        cd_history_file = self.setup_cd_history(cd_history)

        existing_files = [
            cd_history_file,
        ]
        existing_dirs = [
            "/home/user/Downloads",
            "/home/user/dessen",
            "/home/user/doc",
            "/home/user/doc1",
            "/home/user/doc2",
            "/home/user/doc3",
        ]

        mock_isfile.side_effect = self.create_file_checker_mock(existing_files)
        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)

        # using default action
        cli_args = [
            SCRIPT_NAME,
            MODE_ARG, "gui",
        ]
        sys.argv = cli_args
        self.app.delay_start()

        def test():
            self.app.slow_down_reader(0.5)
            self.app.allow_start()
            self.app.wait_until_search_started()
            time.sleep(1)
            unexpected_outputs = [
                "/home/user/Downloads",
                "/home/user/dessen",
                "/home/user/doc",
            ]
            expected_outputs = [
                "/home/user/doc2",
                "/home/user/doc3",
            ]
            displayed = self.app.assert_dirs_displayed(expected_outputs, strict=False)
            for unexpected in unexpected_outputs:
                self.assertNotIn(unexpected, displayed)

            # selecting file 2
            self.app.press_down()
            self.app.press_enter()
            # then
            self.app.wait_until_app_finished()
            self.app.print_stderr()
            self.app.assert_app_finished_with_result(successful=True)
            expected_selection = "/home/user/doc2"
            self.app.assert_printed_to_stdout([expected_selection], strict=True)

        self.executor.start_test_in_process(test)

    @patch('cd_history.file_checker.FileChecker.isdir')
    @patch('cd_history.file_checker.FileChecker.isfile')
    def test_stop_search_then_select_in_gui(self, mock_isfile, mock_isdir):
        # given
        cd_history = textwrap.dedent(f"""
            /home/user/Downloads
            /home/user/dessen
            /home/user/doc
            /home/user/doc1
            /home/user/doc2
            /home/user/doc3
        """).strip()

        cd_history_file = self.setup_cd_history(cd_history)

        existing_files = [
            cd_history_file,
        ]
        existing_dirs = [
            "/home/user/Downloads",
            "/home/user/dessen",
            "/home/user/doc",
            "/home/user/doc1",
            "/home/user/doc2",
            "/home/user/doc3",
        ]

        mock_isfile.side_effect = self.create_file_checker_mock(existing_files)
        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)

        # using default action
        cli_args = [
            SCRIPT_NAME,
            MODE_ARG, "gui",
        ]
        sys.argv = cli_args
        self.app.delay_start()

        def test():
            self.app.slow_down_reader(0.5)
            self.app.allow_start()
            self.app.wait_until_search_started()
            time.sleep(1)
            unexpected_outputs = [
                "/home/user/Downloads",
                "/home/user/dessen",
                "/home/user/doc",
            ]
            expected_outputs = [
                "/home/user/doc2",
                "/home/user/doc3",
            ]
            self.app.assert_dirs_displayed(expected_outputs, strict=False)
            self.app.assert_dirs_not_displayed(unexpected_outputs)

            self.app.press_escape()
            self.app.wait_until_search_done()
            self.app.assert_dirs_not_displayed(unexpected_outputs)

            # selecting file 2
            self.app.press_down()
            self.app.press_enter()
            # then
            self.app.wait_until_app_finished()
            self.app.print_stderr()
            self.app.assert_app_finished_with_result(successful=True)
            expected_selection = "/home/user/doc2"
            self.app.assert_printed_to_stdout([expected_selection], strict=True)

        self.executor.start_test_in_process(test)

    @patch('cd_history.file_checker.FileChecker.isdir')
    @patch('cd_history.file_checker.FileChecker.isfile')
    def test_stop_search_then_exit_in_gui(self, mock_isfile, mock_isdir):
        # given
        cd_history = textwrap.dedent(f"""
            /home/user/Downloads
            /home/user/dessen
            /home/user/doc
            /home/user/doc1
            /home/user/doc2
            /home/user/doc3
        """).strip()

        cd_history_file = self.setup_cd_history(cd_history)

        existing_files = [
            cd_history_file,
        ]
        existing_dirs = [
            "/home/user/Downloads",
            "/home/user/dessen",
            "/home/user/doc",
            "/home/user/doc1",
            "/home/user/doc2",
            "/home/user/doc3",
        ]

        mock_isfile.side_effect = self.create_file_checker_mock(existing_files)
        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)

        # using default action
        cli_args = [
            SCRIPT_NAME,
            MODE_ARG, "gui",
        ]
        sys.argv = cli_args
        self.app.delay_start()

        def test():
            self.app.slow_down_reader(0.5)
            self.app.allow_start()
            self.app.wait_until_search_started()
            time.sleep(1)
            unexpected_outputs = [
                "/home/user/Downloads",
                "/home/user/dessen",
                "/home/user/doc",
            ]
            expected_outputs = [
                "/home/user/doc2",
                "/home/user/doc3",
            ]
            self.app.assert_dirs_displayed(expected_outputs, strict=False)
            self.app.assert_dirs_not_displayed(unexpected_outputs)

            self.app.press_escape()
            self.app.wait_until_search_done()
            self.app.assert_dirs_not_displayed(unexpected_outputs)

            # exit
            self.app.press_escape()
            # then
            self.app.wait_until_app_finished()
            self.app.print_stderr()
            self.app.assert_app_finished_with_result(successful=True)
            self.app.assert_nothing_printed_to_stdout()

        self.executor.start_test_in_process(test)

    @patch('cd_history.file_checker.FileChecker.isdir')
    @patch('cd_history.file_checker.FileChecker.isfile')
    def test_select_dir_while_search_running_in_terminal(self, mock_isfile, mock_isdir):
        # given
        cd_history = textwrap.dedent(f"""
            /home/user/Downloads
            /home/user/dessen
            /home/user/doc
            /home/user/doc1
            /home/user/doc2
            /home/user/doc3
        """).strip()

        cd_history_file = self.setup_cd_history(cd_history)

        existing_files = [
            cd_history_file,
        ]
        existing_dirs = [
            "/home/user/Downloads",
            "/home/user/dessen",
            "/home/user/doc",
            "/home/user/doc1",
            "/home/user/doc2",
            "/home/user/doc3",
        ]

        mock_isfile.side_effect = self.create_file_checker_mock(existing_files)
        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)

        # using default action
        cli_args = [
            SCRIPT_NAME,
            MODE_ARG, "terminal",
        ]
        sys.argv = cli_args
        self.app.delay_start()

        delayed_input = DelayedInput()

        def test():
            self.app.slow_down_reader(0.5)
            self.app.allow_start()
            self.app.wait_until_search_started()
            time.sleep(1)
            unexpected_outputs = [
                "/home/user/Downloads",
                "/home/user/dessen",
            ]
            expected_outputs = [
                "/home/user/doc2",
                "/home/user/doc3",
            ]
            self.app.assert_printed_to_stderr(expected_outputs, strict=False)
            self.app.assert_not_printed_to_stderr(unexpected_outputs)

            # select file 2
            delayed_input.release_input("2\n")
            # then
            self.app.wait_until_app_finished()
            self.app.print_stderr()
            self.app.assert_app_finished_with_result(successful=True)
            expected_selection = "/home/user/doc2"
            self.app.assert_printed_to_stdout([expected_selection], strict=True)

        self.executor.start_test_in_process(test, delayed_input)

    @patch('cd_history.file_checker.FileChecker.isdir')
    @patch('cd_history.file_checker.FileChecker.isfile')
    def test_exit_after_search_in_gui(self, mock_isfile, mock_isdir):
        # given
        cd_history = textwrap.dedent(f"""
            /home/user/Downloads
            /home/user/dessen
            /home/user/doc
        """).strip()

        cd_history_file = self.setup_cd_history(cd_history)

        existing_files = [
            cd_history_file,
        ]
        existing_dirs = [
            "/home/user/Downloads",
            "/home/user/dessen",
            "/home/user/doc",
        ]

        mock_isfile.side_effect = self.create_file_checker_mock(existing_files)
        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)

        # using default action
        cli_args = [
            SCRIPT_NAME,
            MODE_ARG, "gui",
        ]
        sys.argv = cli_args

        def test():
            self.app.wait_until_search_done()
            self.app.wait_until_window_open()
            expected_outputs = [
                "/home/user/doc",
                "/home/user/dessen",
                "/home/user/Downloads",
            ]
            self.app.assert_dirs_displayed(expected_outputs)

            # exit
            self.app.press_escape()
            self.app.wait_until_app_finished()
            self.app.print_stderr()
            self.app.assert_app_finished_with_result(successful=True)
            self.app.assert_nothing_printed_to_stdout()

        self.executor.start_test_in_process(test)

    @patch('cd_history.file_checker.FileChecker.isdir')
    @patch('cd_history.file_checker.FileChecker.isfile')
    def test_stop_search_then_select_in_terminal(self, mock_isfile, mock_isdir):
        # given
        cd_history = textwrap.dedent(f"""
            /home/user/Downloads
            /home/user/dessen
            /home/user/doc
            /home/user/doc1
            /home/user/doc2
            /home/user/doc3
        """).strip()

        cd_history_file = self.setup_cd_history(cd_history)

        existing_files = [
            cd_history_file,
        ]
        existing_dirs = [
            "/home/user/Downloads",
            "/home/user/dessen",
            "/home/user/doc",
            "/home/user/doc1",
            "/home/user/doc2",
            "/home/user/doc3",
        ]

        mock_isfile.side_effect = self.create_file_checker_mock(existing_files)
        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)

        # using default action
        cli_args = [
            SCRIPT_NAME,
            MODE_ARG, "terminal",
        ]
        sys.argv = cli_args

        self.app.delay_start()
        delayed_input = DelayedInput()

        def test():
            self.app.slow_down_reader(0.5)
            self.app.allow_start()
            self.app.wait_until_search_started()
            time.sleep(1)

            # stop search
            delayed_input.release_input("\n")
            self.app.wait_until_search_done()
            unexpected_outputs = [
                "/home/user/Downloads",
                "/home/user/dessen",
            ]
            expected_outputs = [
                "/home/user/doc2",
                "/home/user/doc3",
            ]
            self.app.assert_printed_to_stderr(expected_outputs, strict=False)
            self.app.assert_not_printed_to_stderr(unexpected_outputs)

            # now select item 2
            delayed_input.release_input("2\n")
            self.app.wait_until_app_finished()

            # then
            self.app.print_stderr()
            expected_selection = "/home/user/doc2"
            self.app.assert_printed_to_stdout([expected_selection], strict=True)
            self.app.assert_app_finished_with_result(successful=True)

        self.executor.start_test_in_process(test, delayed_input)

    @patch('cd_history.file_checker.FileChecker.isdir')
    @patch('cd_history.file_checker.FileChecker.isfile')
    def test_stop_search_then_exit_in_terminal(self, mock_isfile, mock_isdir):
        # given
        cd_history = textwrap.dedent(f"""
            /home/user/Downloads
            /home/user/dessen
            /home/user/doc
            /home/user/doc1
            /home/user/doc2
            /home/user/doc3
        """).strip()

        cd_history_file = self.setup_cd_history(cd_history)

        existing_files = [
            cd_history_file,
        ]
        existing_dirs = [
            "/home/user/Downloads",
            "/home/user/dessen",
            "/home/user/doc",
            "/home/user/doc1",
            "/home/user/doc2",
            "/home/user/doc3",
        ]

        mock_isfile.side_effect = self.create_file_checker_mock(existing_files)
        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)

        # using default action
        cli_args = [
            SCRIPT_NAME,
            MODE_ARG, "terminal",
        ]
        sys.argv = cli_args

        self.app.delay_start()
        delayed_input = DelayedInput()

        def test():
            self.app.slow_down_reader(0.5)
            self.app.allow_start()
            self.app.wait_until_search_started()
            time.sleep(1)
            self.assertFalse(self.app.is_search_done())

            # stop search
            delayed_input.release_input("\n")
            self.app.wait_until_search_done()

            unexpected_outputs = [
                "/home/user/Downloads",
                "/home/user/dessen",
            ]
            # at least those
            expected_outputs = [
                "/home/user/doc2",
                "/home/user/doc3",
            ]
            self.app.assert_printed_to_stderr(expected_outputs, strict=False)
            self.app.assert_not_printed_to_stderr(unexpected_outputs)

            # now exit
            delayed_input.release_input("\n")
            self.app.wait_until_app_finished()

    @patch('cd_history.file_checker.FileChecker.isdir')
    @patch('cd_history.file_checker.FileChecker.isfile')
    def test_exit_after_search_in_terminal_via_enter(self, mock_isfile, mock_isdir):
        # given
        cd_history = textwrap.dedent(f"""
            /home/user/Downloads
            /home/user/dessen
            /home/user/doc
        """).strip()

        cd_history_file = self.setup_cd_history(cd_history)

        existing_files = [
            cd_history_file,
        ]
        existing_dirs = [
            "/home/user/Downloads",
            "/home/user/dessen",
            "/home/user/doc",
        ]

        mock_isfile.side_effect = self.create_file_checker_mock(existing_files)
        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)

        # using default action
        cli_args = [
            SCRIPT_NAME,
            MODE_ARG, "terminal",
        ]
        sys.argv = cli_args

        delayed_input = DelayedInput()

        def test():
            self.app.wait_until_search_done()

            expected_outputs = [
                "/home/user/Downloads",
                "/home/user/dessen",
                "/home/user/doc",
            ]
            self.app.assert_printed_to_stderr(expected_outputs, strict=True)

            # now exit via enter
            delayed_input.release_input("\n")
            self.app.wait_until_app_finished()

            # then
            self.app.print_stderr()
            self.app.assert_nothing_printed_to_stdout()
            self.app.assert_app_finished_with_result(successful=True)

        self.executor.start_test_in_process(test, delayed_input)

    @patch('cd_history.file_checker.FileChecker.isdir')
    @patch('cd_history.file_checker.FileChecker.isfile')
    def test_exit_after_search_in_terminal_via_ctrl_c(self, mock_isfile, mock_isdir):
        # given
        cd_history = textwrap.dedent(f"""
            /home/user/Downloads
            /home/user/dessen
            /home/user/doc
        """).strip()

        cd_history_file = self.setup_cd_history(cd_history)

        existing_files = [
            cd_history_file,
        ]
        existing_dirs = [
            "/home/user/Downloads",
            "/home/user/dessen",
            "/home/user/doc",
        ]

        mock_isfile.side_effect = self.create_file_checker_mock(existing_files)
        mock_isdir.side_effect = self.create_dir_checker_mock(existing_dirs)

        # using default action
        cli_args = [
            SCRIPT_NAME,
            MODE_ARG, "terminal",
        ]
        sys.argv = cli_args

        delayed_input = DelayedInput()

        def test():
            self.app.wait_until_search_done()

            expected_outputs = [
                "/home/user/Downloads",
                "/home/user/dessen",
                "/home/user/doc",
            ]
            self.app.assert_printed_to_stderr(expected_outputs, strict=True)

            # now exit via ctrl+c (sigint)
            self.executor.send_sigint()
            self.app.wait_until_app_finished()

            # then
            self.app.print_stderr()
            self.app.assert_nothing_printed_to_stdout()
            self.app.assert_app_finished_with_result(successful=True)

        self.executor.start_test_in_process(test, delayed_input)

    def tearDown(self):
        os.environ = self.default_env
        self.app.teardown()
