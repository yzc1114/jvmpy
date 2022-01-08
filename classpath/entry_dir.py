import classpath.entry as entry
import os


class DirEntry(entry.Entry):

    def __init__(self, path: str):
        self.absDir = os.path.abspath(path)

    @entry.Entry.dec_read_class
    def read_class(self, classname: str) -> (bytes, object, str):
        file_name = os.path.join(self.absDir, classname)
        with open(file_name, 'rb') as f:
            bs = bytes(f.read())
            return bs, self, None

    def to_string(self):
        return self.absDir
