
from textx import metamodel_from_str, metamodel_from_file
from dsl.utils import getGrammar, getGrammarPath


class AstBuilder:
    def __init__(self, grammar, code) -> None:
        assert grammar is not None
        assert code is not None
        self.grammar = grammar
        self.code = code

    def buildAst(self):
        NotImplemented()


class FqlAstBuilder(AstBuilder):
    def __init__(self, grammar, code) -> None:
        super().__init__(grammar, code)
        self.buildAst()

    @staticmethod
    def fqlAstFromCode(code):
        grammarPath = getGrammarPath()
        # grammar = getGrammar() # Add dependency injection
        return FqlAstBuilder(grammarPath, code)

    def buildAst(self):
        metamodel = metamodel_from_file(self.grammar)
        self.fqlAst = metamodel.model_from_str(self.code)

    @property
    def model(self):
        return self.fqlAst
