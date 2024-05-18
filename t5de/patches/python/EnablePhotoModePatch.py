from ...patch import PythonPatch


class EnablePhotoModePatch(PythonPatch):
    def __init__(self):
        super(EnablePhotoModePatch, self).__init__()

        self.register('ENABLE_PHOTO_MODE', 'imvu/mode/ShopMode.py', 'def addChatTool')
        self.register('ENABLE_CHAT_TOOL', 'imvu/mode/ShopMode.py', 'def addChatTool')
        self.register('ENABLE_IN_SHOP_1', 'imvu/client/sessionwindow.py', 'def __hiResSnapshot')
        self.register('ENABLE_IN_SHOP_2', 'imvu/client/sessionwindow.py', 'def __hiResSnapshotNoBg')

    def patch(self, context):
        if context.pattern == 'ENABLE_PHOTO_MODE':
            context.write('@property\n', indent=1)
            context.write('def commonModeUiDisabledFeatures(self):\n', indent=1)
            context.write('return [\'invite-friend\']\n', indent=2)

            context.write(context.line)
        elif context.pattern == 'ENABLE_CHAT_TOOL':
            context.write(context.line)
            context.skip(1)
            context.write('self.addChatToolNoCheck()', indent=2)

            context.write(context.line)
        elif context.pattern == 'ENABLE_IN_SHOP_1':
            context.write(context.line)
            context.skip(2)
        elif context.pattern == 'ENABLE_IN_SHOP_2':
            context.write(context.line)
            context.skip(2)
