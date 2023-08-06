from fqllang.dsl.utils import getGrammar
from fqllang.modules.fqlAstBuilder.ast import FqlAstBuilder
from fqllang.modules.fqlAstTranspiler.postgreTranspiler import FqlAstPostgreSqlTranspiler

GRAMMAR = getGrammar()


def getPostgreCodeFromFqlCode(fqlCode):
    try:
        fqlAstBuilder = FqlAstBuilder.fqlAstFromCode(fqlCode)
        postgreCode = FqlAstPostgreSqlTranspiler(fqlAstBuilder.model)
        return postgreCode
    except:
        raise Exception("Bad Fql Code")


if __name__ == "__main__":
    postgreCode = getPostgreCodeFromFqlCode("get Person with age=5")
    print(postgreCode)
