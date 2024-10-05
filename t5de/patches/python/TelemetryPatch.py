from ...patch import PythonPatch
import base64

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
        self.register('TELEMETRY_10', 'imvu/devicefingerprint.py', r'import')
        self.register('TELEMETRY_11', 'imvu/log.py', r'def getRecords')
        self.register('TELEMETRY_12', 'imvu/mode/HomeMode.py', r'def loadFPEdgeUrl')
        self.register('TELEMETRY_13', 'imvu/account.py', r'def getUpdateInfo')
        self.register('TELEMETRY_14', 'imvu/account.py', r'self\.__factReporter\.recordFact')
        self.register('TELEMETRY_15', 'imvu/account.py', r'self\.__factReporter\.recordFactOnlyOnce')

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
            fp = base64.b64decode("ZGV2aWNlZmluZ2VycHJpbnQucHlk").decode('utf-8')
            context.skip(8)
            context.write('def __load():')
            context.write('import imp, os, sys', indent=2)
            context.write('try:', indent=2)
            context.write('dirname = os.path.dirname(__loader__.archive)', indent=3)
            context.write('except NameError:', indent=2)
            context.write('dirname = sys.prefix', indent=3)
            context.write("path = os.path.join(dirname, \'{}\')".format(fp), indent=2)
            context.write('mod = imp.load_dynamic(__name__, path)', indent=2)
            context.write('__load()')
            context.write('del __load')
        elif context.pattern == 'TELEMETRY_11':
            context.write(context.line)
            context.write('self.clearRecords()', indent=2)
        elif context.pattern == 'TELEMETRY_12':
            context.write(context.line)
            context.skip(5)
            context.write('pass', indent=2)
        elif context.pattern == 'TELEMETRY_13':
            context.write('def shouldRecordFact(self, fact_type):', indent=1)
            context.write('__facts = ["NUI:CreatorMode", "NUI:ProductEditMode", "Create Mode Edit Pid", "Create Mode Derive Pid", "Create Mode Open Chkn", "Create Mode Open Cfl"]', indent=2)
            context.write('if (fact_type in __facts) and not self.chkCreator():', indent=2)
            context.write('return False', indent=3)
            context.write('return True\n\n', indent=2)
            context.write(context.line)
        elif context.pattern in ('TELEMETRY_14', 'TELEMETRY_15'):
            context.write('if self.shouldRecordFact(fact_type):', indent=2)
            context.write(context.line, indent=1)
