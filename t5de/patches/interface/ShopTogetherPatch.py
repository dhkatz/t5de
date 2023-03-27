from ...patch import InterfacePatch


class ShopTogetherPatch(InterfacePatch):
    def __init__(self):
        super(ShopTogetherPatch, self).__init__()

        self.register(
            "DISABLE_UPSELL",
            "dialogs/shop_together_upsell/ShopTogetherUpsell.js",
            r'var imvu'
        )
        self.register(
            "DISABLE_BENEFITS_UPSELL",
            "dialogs/shop_together_extra_benefits_upsell/ShopTogetherUpsell.js",
            r'var imvu'
        )

    def patch(self, context):
        context.write(context.line)
        context.write("    imvu.call('cancelDialog');\n")
        context.seek(context.pattern == "DISABLE_UPSELL" and 22 or 20)
