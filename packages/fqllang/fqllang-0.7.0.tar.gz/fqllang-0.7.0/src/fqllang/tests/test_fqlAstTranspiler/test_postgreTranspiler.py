
from modules.fqlAstBuilder.ast import FqlAstBuilder
from modules.fqlAstTranspiler.postgreTranspiler import FqlAstPostgreSqlTranspiler


class TestFqlAstPostgreSqlTranspiler:
    def test_fqlStatementTranspiler_createForm(self):
        code = "create form Person(name TEXT, age NUMBER, project references Projects)"
        fqlAstBuilder = FqlAstBuilder.fqlAstFromCode(code)
        model = fqlAstBuilder.model
        postgreTanspiler = FqlAstPostgreSqlTranspiler(model)
        result = postgreTanspiler.generate()
        assert result == "CREATE TABLE Person(FQL_ID SERIAL PRIMARY KEY,name VARCHAR(511),age INTEGER,project INTEGER,FOREIGN KEY(project) REFERENCES Projects(FQL_ID));"

    def test_fqlStatementTranspiler_getCase(self):
        code = "get Person"
        fqlAstBuilder = FqlAstBuilder.fqlAstFromCode(code)
        model = fqlAstBuilder.model
        postgreTanspiler = FqlAstPostgreSqlTranspiler(model)
        result = postgreTanspiler.generate()
        assert result == "SELECT * FROM Person;"

    def test_fqlStatementTranspiler_getCaseWithConditions(self):
        code = "get Person with name='Leandro' and age=20"
        fqlAstBuilder = FqlAstBuilder.fqlAstFromCode(code)
        model = fqlAstBuilder.model
        postgreTanspiler = FqlAstPostgreSqlTranspiler(model)
        result = postgreTanspiler.generate()
        assert result == "SELECT * FROM Person WHERE name='Leandro' and age=20;"
        
    def test_fqlStatementTranspiler_createNew(self):
        code = "create Person (name='Leandro', age=23)"
        fqlAstBuilder = FqlAstBuilder.fqlAstFromCode(code)
        model = fqlAstBuilder.model
        postgreTanspiler = FqlAstPostgreSqlTranspiler(model)
        result = postgreTanspiler.generate()
        assert result == "INSERT INTO Person (name,age) VALUES ('Leandro',23);"
