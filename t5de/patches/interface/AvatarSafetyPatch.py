from ...patch import InterfacePatch


class AvatarSafetyPatch(InterfacePatch):
    """
    Enables the mute and boot buttons in the avatar safety dialog.
    """
    def __init__(self):
        super(AvatarSafetyPatch, self).__init__()
        self.register('ENABLE_MUTE', 'dialogs/avatar_safety/avatarSafety.js', r'showMute')
        self.register('ENABLE_BOOT', 'dialogs/avatar_safety/avatarSafety.js', r'showBoot')

    def patch(self, context):
        context.seek(1)
        context.write(context.line)
        context.seek(3)
