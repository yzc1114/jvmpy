import zipfile
from . import entry
import os


class ZipEntry(entry.Entry):

    def __init__(self, path):
        self.abs_path = os.path.abspath(path)

    @entry.Entry.dec_read_class
    def read_class(self, classname: str) -> (bytes, object, str):
        z = zipfile.ZipFile(self.abs_path, 'r')
        for n in z.namelist():
            if n == classname:
                bs = z.read(n)
                return bs, self, None
        raise IOError

    def to_string(self) -> str:
        return self.abs_path
