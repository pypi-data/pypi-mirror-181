
from modules.postgreSqlCodeGenerator.create import CreatePostgreSql
from modules.sqlCodeGenerator.elements import ColumnList, DataConstraint, DataType, Field, FieldList


class TestCreatePostgreSql:

    def test_generate(self):
        tableName = "Person"
        columnList = ColumnList.createColumnListByElements('name', 'age')
        fieldList = FieldList(Field(
            "name", DataType.varchar, DataConstraint.notNull), Field("age", DataType.integer))
        create = CreatePostgreSql(tableName, columnList, fieldList)
        assert create.generate() == "CREATE TABLE Person(name VARCHAR(511) NOT NULL,age INTEGER);"
