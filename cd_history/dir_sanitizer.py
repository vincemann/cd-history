# fix paths that are valid but don't work well with the rest of the program
# stuff like /path//to/my/dir or /path/to/dir/
def sanitize_dir(dir):
    _dir = dir.rstrip()
    _dir = _dir.replace("//", "/")
    if _dir.endswith("/"):
        _dir = _dir[:-1]
    return _dir
