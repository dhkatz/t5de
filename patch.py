class Patch:
    def __init__(self):
        self.file = ""
        self.patterns = {}

    def apply(self, line, pattern, index, source, output):
        return index


class AccountPatch(Patch):
    def __init__(self):
        Patch.__init__(self)
        self.file = "imvu/account"
        self.patterns = {
            'ENABLE_CREATOR': r'def isCreator',
            'DISABLE_CLIENT_ADS': r'def showClientAds',
            'DISABLE_ROOM_ADS': r'def showRoomLoadingAds',
            'DISABLE_LOGS': r'def sendLogsOnLogin'
        }

    def apply(self, line, pattern, index, source, output):
        if pattern == 'ENABLE_CREATOR':
            output.append(line)
            output.append('        return True\n')
            return index + 1
        elif pattern == 'DISABLE_CLIENT_ADS':
            output.append(line)
            output.append('        return False\n')
            return index + 5
        elif pattern == 'DISABLE_ROOM_ADS':
            output.append(line)
            output.append('        return False\n')
            return index + 3
        else:
            output.append(line)
            output.append('        return False\n')
            return index + 1


class ClientAppPatch(Patch):
    def __init__(self):
        Patch.__init__(self)
        self.file = "main/clientapp"
        self.patterns = {
            'DISABLE_LOGS': r"sendLogsOnLogin"
        }

    def apply(self, line, pattern, index, source, output):
        return index + 2


class ProductLoaderPatch(Patch):
    def __init__(self):
        Patch.__init__(self)
        self.file = "imvu/product/productloader"
        self.patterns = {
            'ENABLE_CODES': r'if trialAuth and not'
        }

    def apply(self, line, pattern, index, source, output):
        output.append('        %s\n' % source[index + 4].strip())
        output.append('        %s\n' % source[index + 5].strip())
        return index + 8


class WindowsPatch(Patch):
    def __init__(self):
        Patch.__init__(self)
        self.file = "main/update/windows"
        self.patterns = {
            'DISABLE_UPDATES': r'def updateClientIfNeeded'
        }

    def apply(self, line, pattern, index, source, output):
        output.append(line)
        output.append('    pass\n')
        return index + 19


class SessionWindowPatch(Patch):
    def __init__(self):
        Patch.__init__(self)
        self.file = "imvu/client/sessionwindow"
        self.patterns = {
            'ENABLE_HIRESSNAPSHOT': r'def __hiResSnapshot',
            'ENABLE_HIRESSNAPSHOTNOBG': r'def __hiResSnapshotNoBg'
        }

    def apply(self, line, pattern, index, source, output):
        output.append(line)
        return index + 2
