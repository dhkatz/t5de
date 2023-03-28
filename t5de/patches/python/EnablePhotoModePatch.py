from ...patch import PythonPatch


class EnablePhotoModePatch(PythonPatch):
    def __init__(self):
        super(EnablePhotoModePatch, self).__init__()

        self.register('ENABLE_PHOTO_MODE', 'imvu/mode/Mode.py', 'def commonModeUiDisabledFeatures')

    def patch(self, context):
        context.write(context.line.replace("'photo'", ''))
