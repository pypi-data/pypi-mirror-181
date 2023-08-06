from modules.postgreSqlCodeGenerator.select import SelectPostgreSql, SelectWithCriteriaPostgreSql
from modules.sqlCodeGenerator.elements import Column, ColumnList, Condition, Criteria, Where


class TestSelectPostgreSql:
    def test_generate(self):
        tableName = "Person"
        columnList = ColumnList.createColumnListByElements('name', 'age')
        select = SelectPostgreSql(tableName, columnList)
        print(select)
        assert select.generate() == "SELECT (name,age) FROM Person;"

    def test_generateEmpty(self):
        tableName = "Person"
        columnList = ColumnList.emptyColumnList()
        select = SelectPostgreSql(tableName, columnList)
        print(select)
        assert select.generate() == "SELECT * FROM Person;"


class TestSelectWithCriteriaPostgreSql:
    def test_generateWithEmptyColumnList(self):
        tableName = "Person"
        condition1 = Condition('name', 'Leandro')
        condition2 = Condition('age', 20)
        criteria = Criteria(condition1, condition2)
        columns = ColumnList.emptyColumnList()
        select = SelectWithCriteriaPostgreSql(tableName, columns, criteria)
        assert select.generate() == "SELECT * FROM Person WHERE name='Leandro' and age=20;"

    def test_generateWithColumnList(self):
        tableName = "Person"
        condition1 = Condition('name', 'Leandro')
        condition2 = Condition('age', 20)
        criteria = Criteria(condition1, condition2)
        columns = ColumnList.createColumnListByElements('name', 'firstName')
        select = SelectWithCriteriaPostgreSql(tableName, columns, criteria)
        assert select.generate(
        ) == "SELECT (name,firstName) FROM Person WHERE name='Leandro' and age=20;"
