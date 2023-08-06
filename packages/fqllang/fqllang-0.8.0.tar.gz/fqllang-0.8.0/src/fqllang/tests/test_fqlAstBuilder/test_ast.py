
from modules.fqlAstBuilder.ast import FqlAstBuilder


class TestFqlAstBuilder:
    def test_fqlAstFromCode_createForm(self):
        code = "create form Person(name TEXT, age NUMBER)"
        fqlAstBuilder = FqlAstBuilder.fqlAstFromCode(code)
        assert fqlAstBuilder.model

    def test_fqlAstFromCode_createNew_withNew(self):
        code = "create new Person values (1 , 'Leandro', 'Hernandez')"
        fqlAstBuilder = FqlAstBuilder.fqlAstFromCode(code)
        assert fqlAstBuilder.model

    def test_fqlAstFromCode_createNew_WithoutNew(self):
        code = "create Person values (1 , 'Leandro', 'Hernandez')"
        fqlAstBuilder = FqlAstBuilder.fqlAstFromCode(code)
        assert fqlAstBuilder.model

    def test_fqlAstFromCode_createNew_keyValues(self):
        code = "create Person (number=1 , name='Leandro', H.G.FQL_ID=null, A.FQL_VERSION=2)"
        fqlAstBuilder = FqlAstBuilder.fqlAstFromCode(code)
        assert fqlAstBuilder.model

    def test_fqlAstFromCode_createNew_newkeyValues(self):
        code = "create new Person (number=1 , name='Leandro', H.G.FQL_ID=null, A.FQL_VERSION=2)"
        fqlAstBuilder = FqlAstBuilder.fqlAstFromCode(code)
        assert fqlAstBuilder.model

    def test_fqlAstFromCode_showForms(self):
        code = "show forms Person"
        fqlAstBuilder = FqlAstBuilder.fqlAstFromCode(code)
        assert fqlAstBuilder.model

    def test_fqlAstFromCode_getCase_retrieveAllFormAttributes(self):
        code = "get Person"
        fqlAstBuilder = FqlAstBuilder.fqlAstFromCode(code)
        assert fqlAstBuilder.model

    def test_fqlAstFromCode_getCase_withConditions(self):
        code = "get Person with Person.name=5 and age=24"
        fqlAstBuilder = FqlAstBuilder.fqlAstFromCode(code)
        assert fqlAstBuilder.model

    def test_fqlAstFromCode_getCase_withSomeAttributes(self):
        code = "get Person (code, firstName, age)"
        fqlAstBuilder = FqlAstBuilder.fqlAstFromCode(code)
        assert fqlAstBuilder.model

    def test_fqlAstFromCode_getCase_withConditionsAndSomeAttributes(self):
        code = "get Person (code, firstName, age) with Person.age=1 and firstName='Leandro'"
        fqlAstBuilder = FqlAstBuilder.fqlAstFromCode(code)
        assert fqlAstBuilder.model
