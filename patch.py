class Patch:
    def __init__(self):
        self.file = ""
        self.dir = ""
        self.ext = ""
        self.patterns = {}

    def apply(self, line, pattern, index, source, output):
        return index


class LibraryPatch(Patch):
    def __init__(self):
        Patch.__init__(self)
        self.dir = "library"
        self.ext = "py"


class ContentPatch(Patch):
    def __init__(self):
        Patch.__init__(self)
        self.dir = "imvuContent"
        self.ext = "js"


class AccountPatch(LibraryPatch):
    def __init__(self):
        LibraryPatch.__init__(self)
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


class ClientAppPatch(LibraryPatch):
    def __init__(self):
        LibraryPatch.__init__(self)
        self.file = "main/clientapp"
        self.patterns = {
            'DISABLE_LOGS': r"sendLogsOnLogin"
        }

    def apply(self, line, pattern, index, source, output):
        return index + 2


class ProductLoaderPatch(LibraryPatch):
    def __init__(self):
        LibraryPatch.__init__(self)
        self.file = "imvu/product/productloader"
        self.patterns = {
            'ENABLE_CODES': r'if trialAuth and not'
        }

    def apply(self, line, pattern, index, source, output):
        output.append('        %s\n' % source[index + 4].strip())
        output.append('        %s\n' % source[index + 5].strip())
        return index + 8


class WindowsPatch(LibraryPatch):
    def __init__(self):
        LibraryPatch.__init__(self)
        self.file = "main/update/windows"
        self.patterns = {
            'DISABLE_UPDATES': r'def updateClientIfNeeded'
        }

    def apply(self, line, pattern, index, source, output):
        output.append(line)
        output.append('    pass\n')
        return index + 19


class SessionWindowPatch(LibraryPatch):
    def __init__(self):
        LibraryPatch.__init__(self)
        self.file = "imvu/client/sessionwindow"
        self.patterns = {
            'ENABLE_HIRESSNAPSHOT': r'def __hiResSnapshot',
            'ENABLE_HIRESSNAPSHOTNOBG': r'def __hiResSnapshotNoBg'
        }

    def apply(self, line, pattern, index, source, output):
        output.append(line)
        return index + 2


class ShopTogetherPatch(ContentPatch):
    def __init__(self):
        ContentPatch.__init__(self)
        self.file = 'dialogs/shop_together_extra_benefits_upsell/ShopTogetherUpsell'
        self.patterns = {
            'DISABLE_UPSELL': 'var imvu'
        }

    def apply(self, line, pattern, index, source, output):
        output.append(line)
        output.append("    imvu.call('cancelDialog');\n")
        return index + 20


class ShopTogetherPatch2(ContentPatch):
    def __init__(self):
        ContentPatch.__init__(self)
        self.file = 'dialogs/shop_together_upsell/ShopTogetherUpsell'
        self.patterns = {
            'DISABLE_UPSELL': 'var imvu'
        }

    def apply(self, line, pattern, index, source, output):
        output.append(line)
        output.append("    imvu.call('cancelDialog');")
        return index + 22


class InviteTimePatch(ContentPatch):
    def __init__(self):
        ContentPatch.__init__(self)
        self.file = 'dialogs/invited_to_chat/invited_to_chat'
        self.patterns = {
            'UPDATE_TIME': r'30 \* 1000'
        }

    def apply(self, line, pattern, index, source, output):
        output.append(line.replace('30', '300'))
        return index


class AvatarSafetyPatch(ContentPatch):
    def __init__(self):
        ContentPatch.__init__(self)
        self.file = 'dialogs/avatar_safety/avatarSafety'
        self.patterns = {
            'ENABLE_BOOT': r'showBoot',
            'ENABLE_MUTE': r'showMute'
        }

    def apply(self, line, pattern, index, source, output):
        output.append(source[index + 1])
        return index + 4


class ChatRoomSearchPatch(ContentPatch):
    def __init__(self):
        ContentPatch.__init__(self)
        self.file = 'chat_rooms/ChatRoomSearch'
        self.patterns = {
            'ENABLE_FILTERS': 'Empty Rooms'
        }

    def apply(self, line, pattern, index, source, output):
        output.append(line)
        output.append("        [_T('Non-Empty Rooms'), '1-10'],\n")
        output.append("        [_T('1 Person'), '1'],\n")
        return index
