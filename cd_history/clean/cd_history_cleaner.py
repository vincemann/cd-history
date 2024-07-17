from file_read_backwards import FileReadBackwards

from cd_history.file_checker import FileChecker


class CdHistoryCleaner:

    def __init__(self, hist_file):
        self.hist_file = hist_file
        self.cleaned_lines = []
        self.file_checker = FileChecker()

    def clean(self):
        with FileReadBackwards(self.hist_file) as file:
            while True:
                dir = file.readline()
                if dir == "":  # EOF
                    break
                dir = dir.strip()
                if not dir:
                    continue
                if not self.accept(dir):
                    continue
                self.cleaned_lines.append(dir)
            self.write_lines_to_file()
            file.close()

    def write_lines_to_file(self):
        self.cleaned_lines.reverse()
        if len(self.cleaned_lines) == 0:
            content = ""
        else:
            content = '\n'.join(self.cleaned_lines)+'\n'
        with open(self.hist_file, 'w') as file:
            file.write(content)

    def accept(self, dir):
        if not self.file_checker.isdir(dir):
            return False
        if dir in self.cleaned_lines:
            return False
        return True
