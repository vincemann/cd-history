import unittest

from cd_history.dir_sanitizer import sanitize_dir


class TestDirSanitizer(unittest.TestCase):

    def test_sanitize(self):
        self.assertEqual("/home/user/documents", sanitize_dir("/home/user//documents/"))
        self.assertEqual("/home/user/downloads", sanitize_dir("/home/user//downloads//"))
        self.assertEqual("/home/user/pictures", sanitize_dir("/home/user/pictures"))
        self.assertEqual("/home/user/music", sanitize_dir("/home/user//music/"))

    if __name__ == '__main__':
        unittest.main()
