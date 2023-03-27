from ...patch import PythonPatch


class AccountPatch(PythonPatch):
    def __init__(self):
        super(AccountPatch, self).__init__()

        self.register("ENABLE_CREATOR", "library/imvu/account.py", r'def isCreator')
        self.register("DISABLE_CLIENT_ADS", "library/imvu/account.py", r'def showClientAds')
        self.register("DISABLE_ROOM_ADS", "library/imvu/account.py", r'def showRoomLoadingAds')

    def patch(self, context):
        if context.pattern == "ENABLE_CREATOR":
            context.write(context.line)
            context.write("        return True\n")
            context.seek(1)
        elif context.pattern == "DISABLE_CLIENT_ADS":
            context.write(context.line)
            context.write("        return False\n")
            context.seek(5)
        elif context.pattern == "DISABLE_ROOM_ADS":
            context.write(context.line)
            context.write("        return False\n")
            context.seek(3)
        else:
            context.write(context.line)
            context.write("        return False\n")
            context.seek(1)
