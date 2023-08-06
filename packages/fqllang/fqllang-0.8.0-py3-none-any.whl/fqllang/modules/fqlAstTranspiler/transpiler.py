class AstTranspiler:
    def __init__(self, astModel) -> None:
        self.model = astModel

    def generate(self):
        NotImplemented()


class FqlAstTranspiler(AstTranspiler):
    def __init__(self, fqlAstModel) -> None:
        super().__init__(fqlAstModel)


class FqlAstSqlTranspiler(FqlAstTranspiler):
    def __init__(self, fqlAstModel) -> None:
        super().__init__(fqlAstModel)
