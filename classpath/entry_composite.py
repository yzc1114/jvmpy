# from . import entry
import classpath.entry as entry


class CompositeEntry(entry.Entry):

    def __init__(self, path: str):
        self.entries = []
        for p in path.split(entry.path_list_separator):
            self.entries.append(entry.Entry.new_entry(p))

    @entry.Entry.dec_read_class
    def read_class(self, classname: str) -> (bytes, entry.Entry, str):
        for entry in self.entries:
            data, from_entry, err = entry.read_class(classname)
            if err is None:
                return data, from_entry, err
        return None, None, '没有找到{0}'.format(classname)

    def to_string(self) -> str:
        strs = []
        for e in self.entries:
            strs.append(e.to_string())
        return entry.path_list_separator.join(strs)
