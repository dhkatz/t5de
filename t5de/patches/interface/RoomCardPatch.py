from ...patch import InterfacePatch


class RoomCardPatch(InterfacePatch):
    def __init__(self):
        super(RoomCardPatch, self).__init__()
        self.register('ROOM_CARD_HTML', 'dialogs/room_card/index.html', 'fullness-label')
        self.register('ROOM_CARD_JS', 'dialogs/room_card/roomCard.js', r'results.participants =')
        self.register('ROOM_CARD_CSS', 'dialogs/room_card/roomCard.css', r'\#owner\-label')
        self.register('ROOM_CARD_CSS_2', 'dialogs/room_card/roomCard.css', r'^\#owner-label, \#language-label, \#rating-label')
        self.register('ROOM_CARD_CSS_3', 'dialogs/room_card/roomCard.css', r'^\#owner-name, \#language-name, \#fullness-label')

    def patch(self, context):
        if context.pattern == 'ROOM_CARD_HTML':
            context.write(context.line)
            context.write('<div id="extras-label">', indent=6)
            context.write('<div id="visitors-label"><script id="inline_translate">_iT("Visitors: ", "inline_translate")</script>'
                          '<span class="notranslate"><span id="visitors-count"></span></span></div>', indent=7)
            context.write('<div id="boot_count-label"><script id="inline_translate">_iT("Boot Count: ", "inline_translate")</script>'
                          '<span class="notranslate"><span id="boot-count"></span></span></div>', indent=7)
            context.write('</div>', indent=6)
        elif context.pattern == 'ROOM_CARD_JS':
            context.write("\n")
            context.write('$(\'#visitors-count\').text((results.visitors_count && results.visitors_count >= 0) ? results.visitors_count : "N/A");', indent=3)
            context.write('$(\'#boot-count\').text((results.boot_count && results.boot_count >= 0) ? results.boot_count : "N/A");\n\n', indent=3)
            context.write(context.line)
        elif context.pattern == 'ROOM_CARD_CSS':
            context.write('#extras-label > * {\n')
            context.write('    display: inline-block;\n')
            context.write('}\n\n')
            context.write('#visitors-label {\n')
            context.write('    margin-right: 10px;\n')
            context.write('}\n\n')
            context.write(context.line)
        elif context.pattern == 'ROOM_CARD_CSS_2':
            context.write(context.line.replace(' {', ', #visitors-label, #boot_count-label {'))
        elif context.pattern == 'ROOM_CARD_CSS_3':
            context.write(context.line.replace(' {', ', #visitors-count, #boot-count {'))
