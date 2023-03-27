from ...patch import InterfacePatch


class ShopModePatch(InterfacePatch):
    def __init__(self):
        super(ShopModePatch, self).__init__()

        self.register('SHOPMODE_ADD_ELEMENT', 'shop/ShopMode.js', r'class="more\-info')
        self.register('SHOPMODE_ADD_SELECTOR', 'shop/ShopMode.js', r'dialog\.elMoreInfo =')
        self.register('SHOPMODE_ADD_CONTENT', 'shop/ShopMode.js', r'var categoryNames = \[\];')
        self.register('SHOPMODE_ADD_CSS', 'shop/style.css', r'\.more\-info')

    def patch(self, context):
        if context.pattern == 'SHOPMODE_ADD_ELEMENT':
            context.write(context.line)
            context.write('\'<span class="product-id" data-ui-name="ProductId"></span>\' +\n', indent=2)
        elif context.pattern == 'SHOPMODE_ADD_SELECTOR':
            context.write(context.line)
            context.write('dialog.elProductId = dialog.innerElement.querySelector("span.product-id");\n', indent=1)
        elif context.pattern == 'SHOPMODE_ADD_CONTENT':
            context.write('this.elProductId.innerHTML = "ID: " + product.id;\n', indent=2)
            context.write(context.line)
        elif context.pattern == 'SHOPMODE_ADD_CSS':
            context.write('div#panel_product_info span.product-id {\n')
            context.write('    display: block;\n')
            context.write('    position: absolute;\n')
            context.write('    right: 5px;\n')
            context.write('    bottom: 5px;\n')
            context.write('    color: #000000;\n')
            context.write('    font-size: 11px;\n')
            context.write('    -moz-user-select: text;\n')
            context.write('}\n\n')

            context.write(context.line)
