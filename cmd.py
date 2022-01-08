import argparse


class Cmd(object):
    def __init__(self, version_flag, classpath, Xjre,  class_name, args, verbose_inst, verbose_class):
        self.version_flag: bool = version_flag
        self.classpath: str = classpath
        self.className: str = class_name
        self.args: [] = args
        self.Xjre: str = Xjre
        self.verbose_inst = verbose_inst
        self.verbose_class = verbose_class

    @staticmethod
    def parse_cmd():
        parser = argparse.ArgumentParser()
        parser.description = 'jvmpy'
        parser.add_argument('--version', '-v', action='store_true')
        parser.add_argument('-classpath', '-cp', help='您的类路径', type=str, default='')
        parser.add_argument('className', nargs='?', help='您的主类', default='')
        parser.add_argument('-Xjre', type=str, default='')
        parser.add_argument('args', nargs='*', default=[])
        parser.add_argument('--verbose_inst', action='store_true')
        parser.add_argument('--verbose_class', '-verbose', action='store_true')
        args = parser.parse_args()
        return Cmd(args.version, args.classpath, args.Xjre, args.className, args.args, args.verbose_inst, args.verbose_class)
