from . import Class
from . import Object
from . import Float
from . import Double
from . import String
from . import System
from . import Throwable
from . import Thread


Class.init()
Object.init()
Float.init()
String.init()
System.init()
Double.init()
Throwable.init()
Thread.init()


__all__ = ['Class', 'Object']