from modules.sqlCodeGenerator.elements import Column, ColumnList, Condition, Criteria, DataConstraint, DataType, Field, FieldList, Reference, ValueList, Where


class TestColumnList:
    def test_len(self):
        name = Column('name')
        age = Column('age')
        columnList = ColumnList(name, age)
        assert len(columnList) == 2

    def test_isEmpty(self):
        columnList = ColumnList()
        assert columnList.isEmpty

    def test_transformColumnsInStrList(self):
        name = Column('name')
        age = Column('age')
        columnList = ColumnList(name, age)
        assert columnList.columnsInStrList() == ['name', 'age']

    def test_iter(self):
        name = Column('name')
        age = Column('age')
        columnList = ColumnList(name, age)
        for column, element in zip(columnList, [name, age]):
            assert column == element

    def test_generate(self):
        name = Column('name')
        age = Column('age')
        columnList = ColumnList(name, age)
        assert columnList.generate() == "(name,age)"

    def test_generateEmpty(self):
        columnList = ColumnList()
        assert columnList.generate() == "*"

    def test_createColumnListByElements(self):
        strElements = ["name", "age", "address"]
        columnList = ColumnList.createColumnListByElements(*strElements)
        assert columnList.generate() == "(name,age,address)"
        
class TestValueList:
    def test_generate(self):
        valueList = ValueList.createColumnListByElements(4,"Leandro",True)
        assert valueList.generate() == "(4,'Leandro',True)"


class TestField:
    def test_generate(self):
        name = "name"
        dataType = DataType.varchar
        dataConstraint1 = DataConstraint.notNull
        dataConstraint2 = DataConstraint.unique
        field = Field(name, dataType, dataConstraint1, dataConstraint2)
        assert field.generate() == "name VARCHAR(511) NOT NULL UNIQUE"

    def test_generateWithoutDataConstraints(self):
        name = "name"
        dataType = DataType.varchar
        field = Field(name, dataType)
        assert field.generate() == "name VARCHAR(511)"

    def test_addDataConstraint(self):
        name = "name"
        dataType = DataType.varchar
        field = Field(name, dataType)
        field.addDataConstraint(DataConstraint.primaryKey)
        field.addDataConstraint(DataConstraint.primaryKey)
        assert field.generate() == "name VARCHAR(511) PRIMARY KEY"


class TestCondition:
    def test_generate(self):
        condition1 = Condition('name', 'Leandro')
        condition2 = Condition('age', 20)
        assert condition1.generate() == "name='Leandro'"
        assert condition2.generate() == "age=20"


class TestCriteria:
    def test_generate(self):
        condition1 = Condition('name', 'Leandro')
        condition2 = Condition('age', 20)
        criteria = Criteria(condition1, condition2)
        assert criteria.generate() == "name='Leandro' and age=20"


class TestWhere:
    def test_generate(self):
        condition1 = Condition('name', 'Leandro')
        condition2 = Condition('age', 20)
        criteria = Criteria(condition1, condition2)
        where = Where(criteria)
        assert where.generate() == "WHERE name='Leandro' and age=20"
        

class TestReference:
    def test_generate(self):
        field = Field("Project", DataType.integer)
        refPath = "Projects"
        reference = Reference(field, refPath)
        assert reference.generate() == "Project INTEGER,FOREIGN KEY(Project) REFERENCES Projects(FQL_ID)"


class TestFieldList:
    def test_generate(self):
        field1 = Field("name", DataType.varchar, DataConstraint.notNull)
        field2 = Field("age", DataType.integer)
        field3 = Field("isCold", DataType.boolean)
        fieldList = FieldList(field1, field2, field3)
        assert fieldList.generate() == "name VARCHAR(511) NOT NULL,age INTEGER,isCold BOOLEAN"
        
    def test_generateWithReferences(self):
        field1 = Field("name", DataType.varchar, DataConstraint.notNull)
        
        fieldReference = Field("Project", DataType.integer)
        refPath = "Projects"
        reference = Reference(fieldReference, refPath)
        
        fieldList = FieldList(field1, reference)
        result = "name VARCHAR(511) NOT NULL,Project INTEGER,FOREIGN KEY(Project) REFERENCES Projects(FQL_ID)"
        assert fieldList.generate() == result
        

    def test_fieldsInStrList(self):
        field1 = Field("name", DataType.varchar, DataConstraint.notNull)
        field2 = Field("age", DataType.integer)
        field3 = Field("isCold", DataType.boolean)
        fieldList = FieldList(field1, field2, field3)
        assert fieldList.fieldsInStrList(
        ) == ["name VARCHAR(511) NOT NULL", "age INTEGER", "isCold BOOLEAN"]

    def test_isEmpty(self):
        fieldList = FieldList()
        assert fieldList.isEmpty

    def test_len(self):
        field1 = Field("name", DataType.varchar, DataConstraint.notNull)
        field2 = Field("age", DataType.integer)
        field3 = Field("isCold", DataType.boolean)
        fieldList = FieldList(field1, field2, field3)
        assert len(fieldList) == 3
