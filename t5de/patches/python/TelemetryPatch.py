from ...patch import PythonPatch


class TelemetryPatch(PythonPatch):
    def __init__(self):
        super(TelemetryPatch, self).__init__()

        self.register('TELEMETRY_1', 'imvu/imq/imqconnection.py', r'def __recordPreAuthClose')
        self.register('TELEMETRY_2', 'imvu/mode/ProductEditMode.py', r'self\.__recordSaveException')
        self.register('TELEMETRY_3', 'imvu/mode/SettingsMode.py', r'def handle_sendLogs')
        self.register('TELEMETRY_4', 'imvu/account.py', r'def recordModeOpen')
        self.register('TELEMETRY_5', 'imvu/account.py', r'\'room_id\': room_id')
        self.register('TELEMETRY_6', 'main/bugzilla_submit.py', r'submitImvuBug')
        self.register('TELEMETRY_7', 'main/clientapp.py', r'sendLogsOnLogin')
        self.register('TELEMETRY_8', 'main/SendIMVULogs.py', r'def send')
        self.register('TELEMETRY_9', 'main/SendIMVULogs.py', r'def send_internal')
        self.register('TELEMETRY_10', 'imvu/account.py', r'fingerprint\.deviceFingerprint\(\)')

    def patch(self, context):
        if context.pattern == 'TELEMETRY_1':
            context.write(context.line)
            context.skip(2)
        elif context.pattern == 'TELEMETRY_2':
            pass
        elif context.pattern == 'TELEMETRY_3':
            context.write(context.line)
            context.skip(2)
            context.write('pass', indent=2)
        elif context.pattern == 'TELEMETRY_4':
            context.write(context.line)
            context.skip(2)
            context.write('pass', indent=2)
        elif context.pattern == 'TELEMETRY_5':
            context.write('\'room_id\': \'\'}', indent=3)
        elif context.pattern == 'TELEMETRY_6':
            context.write(context.line)
            context.skip(39)
            context.write('pass', indent=1)
        elif context.pattern == 'TELEMETRY_7':
            context.skip(2)
        elif context.pattern == 'TELEMETRY_8':
            context.write(context.line)
            context.skip(4)
            context.write('pass', indent=1)
        elif context.pattern == 'TELEMETRY_9':
            context.write(context.line)
            context.skip(32)
            context.write('return False', indent=1)
        elif context.pattern == 'TELEMETRY_10':
            fingerprint = 'RlB2NFVFTTZWMmx1Wkc5M2N6b3lMalV1TVM0ekxqQTZPam89'
            context.write('data = base64.b64decode(\'{}\').decode(\'utf-8\')'.format(fingerprint), indent=2)
            context.write('si[\'bluecava_fingerprint\'] = data', indent=2)
