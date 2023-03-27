from ...patch import InterfacePatch


class ChatRoomSearchPatch(InterfacePatch):
    def __init__(self):
        super(ChatRoomSearchPatch, self).__init__()
        self.register('ENABLE_FILTERS', 'chat_rooms/ChatRoomSearch.js', 'Empty Rooms')

    def patch(self, context):
        context.write(context.line)
        context.write("        [_T('Non-Empty Rooms'), '1-10'],\n")
        context.write("        [_T('1 Person'), '1'],\n")
