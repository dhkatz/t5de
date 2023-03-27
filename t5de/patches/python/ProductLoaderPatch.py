from ...patch import PythonPatch


class ProductLoaderPatch(PythonPatch):
    """
    Enables the use of any product with the *use command.
    """

    def __init__(self):
        super(ProductLoaderPatch, self).__init__()

        self.register('ENABLE_USE', 'imvu/product/productloader.py', r'if trialAuth and not')

    def patch(self, context):
        context.seek(4)
        context.write('        {}\n'.format(context.line.strip()))
        context.seek(1)
        context.write('        {}\n'.format(context.line.strip()))
        context.seek(3)
