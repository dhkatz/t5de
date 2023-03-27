from ...patch import PythonPatch


class ClientAppPatch(PythonPatch):
    """
    Disables the sending of logs to IMVU on login.

    """
    def __init__(self):
        super(ClientAppPatch, self).__init__()

        self.register('DISABLE_LOGS', 'main/clientapp.py', r'sendLogsOnLogin')

    def patch(self, context):
        context.seek(2)
