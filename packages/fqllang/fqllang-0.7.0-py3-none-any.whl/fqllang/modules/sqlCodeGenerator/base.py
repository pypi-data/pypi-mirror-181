from modules.sqlCodeGenerator.elements import Field, Criteria, ColumnList


class Sql:
    def __init__(self, tableName: str, columns: ColumnList) -> None:
        self.tableName = tableName
        if columns:
            self.columns = columns
        else:
            self.columns = ColumnList.emptyColumnList()

    def generate(self):
        NotImplemented()


class CreateSql(Sql):
    def __init__(self, tableName: str, columns: ColumnList) -> None:
        super().__init__(tableName, columns)


class SelectSql(Sql):
    def __init__(self, tableName: str, columns: ColumnList) -> None:
        super().__init__(tableName, columns)


class InsertSql(Sql):
    def __init__(self, tableName: str, columns: ColumnList, fields: list[Field]) -> None:
        super().__init__(tableName, columns)

    def _valuesList(self, fields: list[Field], columns: ColumnList):
        pass


class SelectWithCriteriaSql(Sql):
    def __init__(self, tableName: str, columns: ColumnList, criteria: Criteria) -> None:
        super().__init__(tableName, columns)
        self.criteria = criteria


class SelectWithMatchSql(Sql):
    def __init__(self, tableName: str, columns: ColumnList, pattern: str) -> None:
        super().__init__(tableName, columns)


class FindByKeySql(Sql):
    def __init__(self, tableName: str, columns: ColumnList, keyColumn: str, keyValue: str):
        super().__init__(tableName, columns)


class PreparedInsertSql(Sql):
    def __init__(self, tableName: str, columns: ColumnList) -> None:
        super().__init__(tableName, columns)

    def _placeholderList(self, columns: ColumnList):
        pass
