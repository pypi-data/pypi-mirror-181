import sys

from .freeze_time import ForbiddenTimePatchFinder
from .patch_call import ForbiddenPatchCallFinder

if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata


class Plugin(object):
    name = "flake8_iw"
    version = importlib_metadata.version("flake8_iw")

    def __init__(self, tree):
        self.tree = tree

    def run(self):
        parser = ForbiddenPatchCallFinder(self.tree)
        parser.visit(self.tree)

        for lineno, column, msg in parser.issues:
            yield (lineno, column, msg, Plugin)

        parser = ForbiddenTimePatchFinder(self.tree)
        parser.visit(self.tree)

        for lineno, column, msg in parser.issues:
            yield (lineno, column, msg, Plugin)
