from cmd import Cmd
from jvm import JVM


if __name__ == '__main__':
    cmd = Cmd.parse_cmd()
    if cmd.version_flag:
        print('version 0.0.1')
    elif cmd.className == '':
        print("主类不能为空")
    else:
        JVM(cmd).start()
