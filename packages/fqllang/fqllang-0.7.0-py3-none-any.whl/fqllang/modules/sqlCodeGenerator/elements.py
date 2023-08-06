from enums import Enum

DataType = Enum("DataType", integer="INTEGER",
                varchar="VARCHAR(511)", boolean="BOOLEAN", serial="SERIAL")

PostgreSqlDataType = Enum("DataType", integer="INTEGER",
                          varchar="VARCHAR(511)", boolean="BOOLEAN", serial="SERIAL")

FqlDataType = Enum("FqlDataType", number="NUMBER",
                   text="TEXT", boolean="BOOLEAN")

DataConstraint = Enum("DataConstraint", notNull="NOT NULL",
                      unique="UNIQUE", primaryKey="PRIMARY KEY")


def convertFqlDataTypeToPostgreSqlDataType(fqlDataType):
    try:
        fql_sql_dict = {
            "NUMBER": PostgreSqlDataType.integer,
            "TEXT": PostgreSqlDataType.varchar,
            "BOOLEAN": PostgreSqlDataType.boolean
        }
        return fql_sql_dict[fqlDataType]
    except Exception as e:
        raise e


class Condition:
    def __init__(self, attribute, value) -> None:
        self.attribute = attribute
        if isinstance(value, str):
            self.value = f"'{value}'"
        else:
            self.value = value

    def generate(self):
        return f"{self.attribute}={self.value}"

    def __str__(self) -> str:
        return self.generate()


class Criteria:
    def __init__(self, *conditions) -> None:
        self.conditions = conditions

    def generate(self):
        conditionsToStrList = self.transformConditionsToStrList()
        return ' and '.join(conditionsToStrList)

    def transformConditionsToStrList(self):
        result = []
        for condition in self.conditions:
            result.append(condition.generate())
        return result

    def __str__(self) -> str:
        return self.generate()


class Where:
    def __init__(self, criteria: Criteria) -> None:
        self.criteria = criteria

    def generate(self):
        return f"WHERE {self.criteria}"

    def __str__(self) -> str:
        return self.generate()


class Field:
    def __init__(self, name: str, dataType, *dataConstraints):
        self.name = name
        self.dataType = dataType.value
        self.dataConstraints = list(map(lambda x: x.value, dataConstraints))

    def addDataConstraint(self, dataConstraint):
        if not self.existDataConstraint(dataConstraint):
            self.dataConstraints.append(dataConstraint.value)

    def existDataConstraint(self, dataConstraint):
        dataConstraintValue = dataConstraint.value
        for value in self.dataConstraints:
            if value == dataConstraintValue:
                return True
        return False

    def generate(self):
        fieldElements = [self.name, self.dataType, *self.dataConstraints]
        result = " ".join(fieldElements)
        return result

    def __str__(self):
        return self.generate()

class Reference:
    def __init__(self, field:Field, refPath:str) -> None:
        self.field = field
        self.refPath = refPath
        
    def generate(self):
        fieldStr = self.field.generate()
        referenceStr = self.generateReferenceStr()
        return f"{fieldStr},{referenceStr}"
    
    def generateReferenceStr(self):
        fieldName = self.field.name
        fqlId = "FQL_ID"
        refPath = self.refPath
        return f"FOREIGN KEY({fieldName}) REFERENCES {refPath}({fqlId})"
    
    


class FieldList:
    def __init__(self, *fields) -> None:
        self.fields = fields

    def generate(self):
        fieldElementsStrList = self.fieldsInStrList()
        result = ",".join(fieldElementsStrList)
        return result

    def fieldsInStrList(self):
        fieldElementsStrList = map(lambda x: x.generate(), self)
        return list(fieldElementsStrList)

    def addField(self, field):
        self.fields.append(field)

    def __iter__(self):
        for field in self.fields:
            yield field

    @property
    def isEmpty(self):
        return len(self) == 0

    def __len__(self):
        return len(self.fields)

    def __str__(self) -> str:
        return self.generate()


class Column:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


class ColumnList:
    def __init__(self, *columns) -> None:
        self.columns = columns

    @staticmethod
    def createColumnListByElements(*elements):
        columns = map(Column, elements)
        return ColumnList(*columns)

    @staticmethod
    def emptyColumnList():
        return ColumnList()

    def generate(self):
        if self.isEmpty:
            return "*"
        columnsInStr = self.columnsInStrList()
        result = "(" + ",".join(columnsInStr) + ")"
        return result

    @property
    def isEmpty(self):
        return len(self) == 0

    def __len__(self):
        return len(self.columns)

    def columnsInStrList(self):
        result = map(str, self)
        return list(result)

    def __iter__(self):
        for column in self.columns:
            yield column

    def __str__(self) -> str:
        return self.generate()
    
class ValueList(ColumnList):
    def __init__(self, *values) -> None:
        super().__init__(*values)
        
    @staticmethod
    def createColumnListByElements(*elements):
        def valueInStr(value):
            if isinstance(value, str):
                return f"'{value}'"
            return str(value)
        columns = map(lambda element: Column(valueInStr(element)), elements)
        return ColumnList(*columns)
    

