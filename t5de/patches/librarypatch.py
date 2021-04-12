import os
import shutil
import zipfile

from uncompyle6 import decompile_file
from py_compile import compile as compile_file

from t5de.patches.patch import Patch


class LibraryPatch(Patch):
    def __init__(self):
        Patch.__init__(self)
        self.dir = "library"
        self.ext = ".py"


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


class BugReportPatch(LibraryPatch):
    def __init__(self):
        LibraryPatch.__init__(self)
        self.file = 'main/bugzilla_submit'
        self.patterns = {
            'DISABLE_BUGREPORTS': r'submitImvuBug'
        }

    def apply(self, line, pattern, index, source, output):
        output.append(line)
        output.append('    pass')
        return index + 41


PATCHES = [AccountPatch(), ClientAppPatch(), ProductLoaderPatch(), WindowsPatch(), SessionWindowPatch(),
           BugReportPatch()]


def setup(cwd):
    print('EXTRACTING: LIBRARY.ZIP')
    with zipfile.ZipFile('{}/IMVUClient/library.zip'.format(cwd), 'r') as zip_file:
        zip_file.extractall('{}/library'.format(cwd))

    for p in PATCHES:
        print('DECOMPILING: {}'.format(p.file))
        with open(os.path.join(cwd, p.dir, p.file + p.ext), "w") as f:
            decompile_file(os.path.join(cwd, p.dir, p.file + '.pyo'), f)


def patches():
    return PATCHES


def cleanup(cwd):
    for p in PATCHES:
        print('COMPILING: {}'.format(p.file))

        compile_file(
            os.path.join(cwd, p.dir, p.file + p.ext), os.path.join(cwd, p.dir, p.file + '.pyo'), '-o', doraise=True
        )

    for p in PATCHES:
        print('CLEANING: {}'.format(p.file))
        filepath = os.path.join(cwd, 'library', p.file + p.ext)
        if os.path.isfile(filepath):
            os.remove(filepath)

    print('ARCHIVING: LIBRARY.ZIP')

    lib_dir = os.path.join(cwd, 'library')

    with zipfile.ZipFile(os.path.join(cwd, 'library.zip'), 'w', compression=zipfile.ZIP_STORED) as zip_file:
        for root, dirs, files in os.walk(lib_dir):
            for filename in files:
                filepath = os.path.join(root, filename)
                zip_file.write(filepath, os.path.relpath(filepath, lib_dir))

    print('ARCHIVED: LIBRARY.ZIP')

    print('REPLACING: LIBRARY.ZIP')

    os.remove(os.path.join(cwd, 'IMVUClient', 'library.zip'))
    shutil.move(os.path.join(cwd, 'library.zip'), os.path.join(cwd, 'IMVUClient'))

    shutil.rmtree(os.path.join(cwd, 'library'))
