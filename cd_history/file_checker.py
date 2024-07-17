import os


class FileChecker:

    def isfile(self, path):
        return os.path.isfile(path)

    def isdir(self, path):
        isdir = os.path.isdir(path)
        if isdir:
            return True
        # isdir might return false if dir is just inaccessible
        # so performing another sneaky check
        try:
            os.listdir(path)
            return True
        except PermissionError:
            # dir exists but user cant read
            return True
        except FileNotFoundError:
            return False


