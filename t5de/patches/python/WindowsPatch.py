from ...patch import PythonPatch


class WindowsPatch(PythonPatch):
    """
    Disables the Windows update check.
    """

    def __init__(self):
        super(WindowsPatch, self).__init__()

        self.register('DISABLE_UPDATES', 'main/update/windows.py', r'def updateClientIfNeeded')

    def patch(self, context):
        context.write(context.line)
        context.write('    pass\n')
        context.seek(19)
