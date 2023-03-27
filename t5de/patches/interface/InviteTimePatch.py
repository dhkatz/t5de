from ...patch import InterfacePatch


class InviteTimePatch(InterfacePatch):
    def __init__(self):
        super(InviteTimePatch, self).__init__()

        self.register(
            "UPDATE_TIME",
            "dialogs/invited_to_chat/invited_to_chat.js",
            r'30 \* 1000'
        )

    def patch(self, context):
        context.write(context.line.replace('30', '300'))
