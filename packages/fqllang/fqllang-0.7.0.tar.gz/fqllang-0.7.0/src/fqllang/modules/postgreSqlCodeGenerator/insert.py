from modules.sqlCodeGenerator.base import InsertSql, PreparedInsertSql
from modules.sqlCodeGenerator.elements import Field, ColumnList, ValueList


class InsertPostgreSql(InsertSql):
    def __init__(self, tableName: str, columns: ColumnList, fields: list[Field]) -> None:
        super().__init__(tableName, columns, fields)

    def _valuesList(self, fields: list[Field], columns: ColumnList):
        pass


class PreparedInsertPostgreSql(PreparedInsertSql):
    def __init__(self, tableName: str, columns: ColumnList, values: ValueList) -> None:
        super().__init__(tableName, columns)
        self.values = values

    def _placeholderList(self, columns: ColumnList):
        pass
    
    def generate(self):
        return f"INSERT INTO {self.tableName} {self.columns} VALUES {self.values};"
    
    def __str__(self) -> str:
        return self.generate()
