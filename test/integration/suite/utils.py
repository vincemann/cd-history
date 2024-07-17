import io
import os


def assert_last_line_of_file_is(file_path, expected_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if not lines:
            return False  # File is empty
        actual_last_line = lines[-1].strip()
        assertEqual(expected_line.strip(), actual_last_line, "last lines of file: '%s' did not match." % file_path)


def assert_printed_to_stream(stream_buf: io.StringIO, expected_outputs, strict=True):
    stream_lines = stream_buf.getvalue().splitlines()
    if stream_lines is None:
        raise AssertionError("stream does not have any lines")
    for file in expected_outputs:
        assertIn(file, str(stream_lines))
    if strict:
        assertEqual(len(expected_outputs), len(stream_lines), "amount of lines printed to output stream did not match."
                                                              " Expected %d, got %d" % (
                    len(expected_outputs), len(stream_lines)))
    return stream_lines


# give me file name of file in test/files and this function resolves it to abs path
def resolve_test_file_path(filename):
    return os.path.join(os.path.dirname(__file__) + "/../../files/", filename)


def assertEqual(first, second, msg=None):
    if first != second:
        raise AssertionError(msg or f"{first} != {second}")


def assertIn(member, container, msg=None):
    if member not in container:
        raise AssertionError(msg or f"{member} not found in {container}")


def assertNotIn(member, container, msg=None):
    if member in container:
        raise AssertionError(msg or f"unexpected {member} found in {container}")
