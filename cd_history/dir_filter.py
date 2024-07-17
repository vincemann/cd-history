import re

from cd_history.file_checker import FileChecker
from cd_history.logging_config import configure_logger


class DirFilter:

    def __init__(self, filter):
        self.logger = configure_logger(self.__class__.__name__)
        self.dirs_read = []
        self.filter = filter
        self.filter_active = filter is not None and filter.strip() is not None
        self.file_checker = FileChecker()

    def accept(self, dir):
        self.logger.debug("checking dir: %s" % dir)
        if self.already_seen(dir):
            self.logger.debug("dir already seen: %s" % dir)
            return False
        self.dirs_read.append(dir)
        if self.filter_active and self.is_ignored_by_filter(dir):
            return False
        if self.is_rel_path(dir):
            self.logger.debug("dir is not abs path: %s" % dir)
            return False
        if not self.is_existing_dir(dir):
            self.logger.debug("dir is not an existing directory: %s" % dir)
            return False
        return True

    def already_seen(self, dir):
        return dir in self.dirs_read

    def is_rel_path(self, dir):
        return not dir.startswith("/")

    def is_ignored_by_filter(self, dir):
        return not re.search(self.filter, dir)

    def is_existing_dir(self, dir):
        return self.file_checker.isdir(dir)


