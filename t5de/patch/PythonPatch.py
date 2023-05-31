import os

from uncompyle6 import decompile_file
from py_compile import compile as compile_file

from t5de.patch.Patch import Patch


class PythonPatch(Patch):
    def register(self, name, filename, pattern):
        if filename.startswith("library/"):
            filename = filename[8:]

        super(PythonPatch, self).register(name, "library/{}".format(filename), pattern)

    def setup(self, context):
        for p in self.replacements:
            if not p.path.endswith('.py'):
                continue

            if os.path.isfile(os.path.join(context.cwd, p.path)):
                continue  # Already decompiled

            print('DECOMPILING: {}'.format(p.path))

            with open(os.path.join(context.cwd, p.path), "w") as f:
                decompile_file(
                    os.path.join(context.cwd, os.path.splitext(p.path)[0] + '.pyo'),
                    f,
                    showasm=False
                )

    def cleanup(self, context):
        for p in self.replacements:
            if not p.path.endswith('.py'):
                continue

            if not os.path.isfile(os.path.join(context.cwd, p.path)):
                continue  # Already compiled

            print('COMPILING: {}'.format(p.path))

            compile_file(
                os.path.join(context.cwd, p.path),
                os.path.join(context.cwd, os.path.splitext(p.path)[0] + '.pyo'),
                '-o',
                doraise=True
            )

            print('CLEANING: {}'.format(p.path))

            filepath = os.path.join(context.cwd, p.path)
            if os.path.isfile(filepath):
                os.remove(filepath)
