from abc import abstractmethod, ABCMeta
import os

path_list_separator = os.path.pathsep


class Entry(metaclass=ABCMeta):

    @abstractmethod
    def read_class(self, classname: str) -> (bytes, object, str):
        pass

    @abstractmethod
    def to_string(self) -> str:
        pass

    @staticmethod
    def new_entry(path: str):
        if path_list_separator in path:
            return entry_composite.CompositeEntry(path)
        elif path.endswith('*'):
            return entry_wildcard.WildcardEntry(path)
        elif path.endswith('.jar') \
                or path.endswith('.JAR') \
                or path.endswith('.zip') \
                or path.endswith('ZIP'):
            return entry_zip.ZipEntry(path)
        else:
            return entry_dir.DirEntry(path)

    @staticmethod
    def dec_read_class(read_class):
        def wrapper(self: Entry, classname: str) -> (bytes, object, str):
            try:
                return read_class(self, classname)
            except Exception:
                return None, None, '读取{0}时失败'.format(classname)
        return wrapper


from . import entry_composite, entry_wildcard, entry_dir, entry_zip