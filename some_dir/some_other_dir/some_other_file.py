import site
from some_dir.some_file import *
import sys
if __name__ == '__main__':
    print(sys.base_exec_prefix)
    print(sys.base_prefix)
    print(sys.prefix)
    print(sys.path)
    A()
    ...