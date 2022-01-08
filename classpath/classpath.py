import os
from . import entry, entry_wildcard


class Classpath(object):

    def __init__(self):
        self.bootClasspath: entry.Entry = None
        self.extClasspath: entry.Entry = None
        self.userClasspath: entry.Entry = None

    @staticmethod
    def parse(jre_option: str, cp_option: str) -> object:
        cp = Classpath()
        cp.__parse_boot_and_ext_classpath(jre_option)
        cp.__parse_user_classpath(cp_option)
        return cp

    def read_class(self, classname) -> (bytes, entry.Entry, str):
        classname += '.class'
        data, from_entry, err = self.bootClasspath.read_class(classname)
        if err is None:
            return data, from_entry, err
        data, from_entry, err = self.extClasspath.read_class(classname)
        if err is None:
            return data, from_entry, err
        return self.userClasspath.read_class(classname)

    def __parse_boot_and_ext_classpath(self, jre_option: str):
        jre_dir = self.__get_jre_dir(jre_option)

        # jre/lib/*
        jre_lib_path = os.path.join(jre_dir, 'lib', '*')
        self.bootClasspath = entry_wildcard.WildcardEntry(jre_lib_path)
        # jre/lib/ext/*
        jre_ext_path = os.path.join(jre_dir, 'lib', 'ext', '*')
        self.extClasspath = entry_wildcard.WildcardEntry(jre_ext_path)

    def __parse_user_classpath(self, cp_option: str):
        if cp_option == '':
            cp_option = '.'
        self.userClasspath = entry.Entry.new_entry(cp_option)

    def to_string(self) -> str:
        return self.userClasspath.to_string()

    def __get_jre_dir(self, jre_option) -> str:
        if jre_option != '' and self.__exists(jre_option):
            return jre_option
        if self.__exists('./jre'):
            return './jre'
        java_home = os.environ.get('JAVA_HOME')
        if java_home != '':
            return os.path.join(java_home, 'jre')
        raise Exception("Can't find jre folder")

    @staticmethod
    def __exists(path) -> bool:
        return os.path.exists(path)
