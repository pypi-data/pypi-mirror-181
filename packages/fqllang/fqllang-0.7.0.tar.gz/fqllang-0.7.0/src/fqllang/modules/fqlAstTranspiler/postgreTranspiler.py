

from dsl.utils import getClassName
from modules.fqlAstTranspiler.transpiler import FqlAstSqlTranspiler
from modules.postgreSqlCodeGenerator.create import CreatePostgreSql
from modules.postgreSqlCodeGenerator.insert import PreparedInsertPostgreSql
from modules.postgreSqlCodeGenerator.select import SelectPostgreSql, SelectWithCriteriaPostgreSql
from modules.sqlCodeGenerator.elements import Column, ColumnList, Condition, Criteria, DataConstraint, DataType, Field, FieldList, Reference, ValueList, convertFqlDataTypeToPostgreSqlDataType


class FqlAstPostgreSqlTranspiler(FqlAstSqlTranspiler):
    def __init__(self, fqlAstModel) -> None:
        super().__init__(fqlAstModel)

    def generate(self):
        return self.fqlStatementTranspiler(self.model)

    def __str__(self) -> str:
        return self.generate()

    def fqlStatementTranspiler(self, model):
        className = getClassName(model)
        if className == "CreateForm":
            return self.createFormTranspiler(model).generate()
        elif className == "CreateNew":
            return self.createNewTranspiler(model).generate()
        elif className == "ShowForms":
            return self.showFormsTranspiler(model).generate()
        elif className == "GetCase":
            return self.getCaseTranspiler(model).generate()
        raise Exception("Modelo incorrecto")

    def createFormTranspiler(self, createForm):
        formName = createForm.formName

        dataSpecList = self.dataSpecListTranspiler(createForm.dataSpecList)

        keyField = Field('FQL_ID', DataType.serial, DataConstraint.primaryKey)
        
        fieldList = FieldList(keyField, *dataSpecList)

        return CreatePostgreSql(formName, ColumnList.emptyColumnList(), fieldList)

    def dataSpecListTranspiler(self, dataSpecList):
        dataSpecListTranspiled = map(lambda dataSpec: self.dataSpecTranspiler(
            dataSpec), dataSpecList)
        return list(dataSpecListTranspiled)
    
    def dataSpecTranspiler(self, dataSpec):
        className = getClassName(dataSpec)
        if className == "DataDefinition":
            return self.dataDefinitionTranspiler(dataSpec)
        elif className == "DataReference":
            return self.dataReferenceTranspiler(dataSpec)

    def dataDefinitionTranspiler(self, dataDefinition):
        dataName = dataDefinition.dataName
        dataType = convertFqlDataTypeToPostgreSqlDataType(
            dataDefinition.dataType)
        notNull = dataDefinition.notNull
        unique = dataDefinition.unique
        field = Field(dataName, dataType)
        if notNull:
            field.addDataConstraint(DataType.notNull)
        if unique:
            field.addDataConstraint(DataType.unique)
        return field

    def dataReferenceTranspiler(self, dataReference):
        dataName = dataReference.dataName
        refCardinality = dataReference.refCardinality
        refPath = dataReference.refPath
        basicField = Field(dataName, DataType.integer)
        reference = Reference(basicField, refPath)
        return reference

    def createNewTranspiler(self, createNew):
        formName = createNew.formName
        columns, values = self.createNewValuesTranspiler(createNew.createNewValues)
        return PreparedInsertPostgreSql(formName, columns, values)

    def createNewValuesTranspiler(self, createNewValues):
        keyValueEntryList = createNewValues.keyValueEntryList
        keyValueList = [self.keyValueEntryTranspiler(keyValueEntry) for keyValueEntry in keyValueEntryList]
        columns = []
        values = []
        for key, value in keyValueList:
            columns.append(key)
            values.append(value)
        return ColumnList.createColumnListByElements(*columns), ValueList.createColumnListByElements(*values)
        
    def keyValueEntryTranspiler(self, keyValueEntry):
        className = getClassName(keyValueEntry)
        if className == "KeyValueSimple":
            return self.keyValueSimpleTranspiler(keyValueEntry)
        elif className == "KeysSeparatesWithDots":
            pass
        
    def keyValueSimpleTranspiler(self, keyValueSimple):
        key = keyValueSimple.key
        valueTerminal = keyValueSimple.valueTerminal
        return key, valueTerminal

    def getCaseTranspiler(self, getCase):
        formName = getCase.formName
        conditions = self.extractConditions(getCase)
        if conditions:
            criteria = self.getCaseConditionsTranspiler(conditions)
            return SelectWithCriteriaPostgreSql(formName, ColumnList.emptyColumnList(), criteria)
        else:
            return SelectPostgreSql(formName)
        # extendedLabelsList = self.extractExtendedLabelsList(getCase)

    def getCaseConditionsTranspiler(self, conditions):
        conditionList = []
        for condition in conditions:
            className = getClassName(condition)
            if className == "ConditionTerminal":
                attribute = condition.attribute
                valueTerminal = condition.valueTerminal
                conditionList.append(Condition(attribute, valueTerminal))
        return Criteria(*conditionList)

    def extractConditions(self, getCase):
        try:
            return getCase.conditions
        except:
            return []

    # def extractExtendedLabelsList(self, getCase):
    #     try:
    #         return getCase.extendedLabelsList
    #     except:
    #         return []

    def showFormsTranspiler(self, showForms):
        pass
