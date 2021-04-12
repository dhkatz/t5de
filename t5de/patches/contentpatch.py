import os
import shutil
import zipfile

from patch import Patch


class ContentPatch(Patch):
    def __init__(self):
        Patch.__init__(self)
        self.dir = "imvuContent"
        self.ext = ".js"


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


PATCHES = [ShopTogetherPatch(), ShopTogetherPatch2(), InviteTimePatch(), AvatarSafetyPatch(), ChatRoomSearchPatch()]


def setup(cwd):
    print ('EXTRACTING: IMVUCONTENT.jar')
    with zipfile.ZipFile('{}/IMVUClient/ui/chrome/imvuContent.jar'.format(cwd), 'r') as zip_file:
        zip_file.extractall(os.path.join(cwd, 'imvuContent'))


def patches():
    return PATCHES


def cleanup(cwd):
    print('ARCHIVING: IMVUCONTENT.JAR')

    content_dir = os.path.join(cwd, 'imvuContent')

    with zipfile.ZipFile(os.path.join(cwd, 'imvuContent.jar'), 'w', compression=zipfile.ZIP_STORED) as zip_file:
        for root, dirs, files in os.walk(content_dir):
            for filename in files:
                filepath = os.path.join(root, filename)
                zip_file.write(filepath, os.path.relpath(filepath, content_dir))

    print('ARCHIVED: IMVUCONTENT.JAR')

    print('REPLACING: IMVUCONTENT.jar')

    os.remove(os.path.join(cwd, 'IMVUClient/ui/chrome', 'imvuContent.jar'))
    shutil.move(os.path.join(cwd, 'imvuContent.jar'), os.path.join(cwd, 'IMVUClient/ui/chrome'))

    shutil.rmtree(os.path.join(cwd, 'imvuContent'))
