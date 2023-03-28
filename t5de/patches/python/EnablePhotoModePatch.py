from ...patch import PythonPatch


class EnablePhotoModePatch(PythonPatch):
    def __init__(self):
        super(EnablePhotoModePatch, self).__init__()

        self.register('ENABLE_PHOTO_MODE', 'imvu/mode/ShopMode.py', 'def addChatTool')

    def patch(self, context):
        if context.pattern == 'ENABLE_PHOTO_MODE':
            context.write('@property\n', indent=1)
            context.write('def commonModeUiDisabledFeatures(self):\n', indent=1)
            context.write('return [\'invite-friend\']\n', indent=2)

            context.write(context.line)
