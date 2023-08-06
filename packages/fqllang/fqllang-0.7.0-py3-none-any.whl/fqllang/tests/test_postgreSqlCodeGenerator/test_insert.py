
from modules.postgreSqlCodeGenerator.insert import PreparedInsertPostgreSql
from modules.sqlCodeGenerator.elements import ColumnList, ValueList


class TestPreparedInsertPostgreSql:
    def test_generate(self):
        tableName = "Person"
        columnList = ColumnList.createColumnListByElements('name', 'age')
        valueList = ValueList.createColumnListByElements('Leandro', 23)
        insert = PreparedInsertPostgreSql(tableName, columnList, valueList)
        assert insert.generate() == "INSERT INTO Person (name,age) VALUES ('Leandro',23);"
