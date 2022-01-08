import classpath.entry_composite as entry_composite
import classpath.entry_zip as entry_zip
import os


class WildcardEntry(entry_composite.CompositeEntry):

    def __init__(self, path):
        self.baseDir = path[:-1]
        self.entries = []
        for root, dirs, files in os.walk(self.baseDir):
            for filename in files:
                if filename.endswith('.jar') or filename.endswith('.JAR'):
                    self.entries.append(entry_zip.ZipEntry(os.path.join(root, filename)))
