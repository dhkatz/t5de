from ...patch import InterfacePatch


class AvatarCardPatch(InterfacePatch):
    """
    Enables the mute and boot buttons in the avatar safety dialog.
    """
    def __init__(self):
        super(AvatarCardPatch, self).__init__()
        self.register('AVATAR_CARD_HTML', 'dialogs/avatar_card/index.html', 'Here for:')
        self.register('AVATAR_CARD_JS', 'dialogs/avatar_card/avatarCard.js', r'this\.elLookingFor =')
        self.register('AVATAR_CARD_JS_2', 'dialogs/avatar_card/avatarCard.js', r'if \(info\.dating\.drinking\)')
        self.register('AVATAR_CARD_CSS', 'dialogs/avatar_card/avatarCard.css', r'^\.editmode \.affinity-item \.text')

    def patch(self, context):
        if context.pattern == 'AVATAR_CARD_HTML':
            context.write(context.line)
            context.write('<div class="affinity-item"><label>CID:</label><div class="text"><span '
                          'id="cid" class="no-edit"></span></div></div>\n', indent=7)
        elif context.pattern == 'AVATAR_CARD_JS':
            context.write(context.line)
            context.write('this.elCid = find("#cid");\n', indent=1)
        elif context.pattern == 'AVATAR_CARD_JS_2':
            context.write('this.elCid.innerHTML = this.cid.toString();\n', indent=3)
            context.write('while (this.elCid.clientHeight > 12) {\n', indent=3)
            context.write('adjustTextSize(this.elCid, -1);\n', indent=4)
            context.write('}\n', indent=3)
            context.write(context.line)
        elif context.pattern == 'AVATAR_CARD_CSS':
            context.write(context.line.replace('span', 'span:not(.no-edit)'))
