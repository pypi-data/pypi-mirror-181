
from dsl.fql.createForm import Form
from dsl.utils import getClassName
from dsl.fql.base import Field, Reference, RefCardinality, RefConstraint, SimpleId, DataPath, All, DataLabelList, DataLabel


class ModelAnalizer:
    def __init__(self, model) -> None:
        self.model = model
        
    def analizeModel(self):
        className = getClassName(self.model)
        if className == "CreateForm":
            return self.analizeCreateForm(self.model)
            
    def analizeCreateForm(self, createForm):
        formName = createForm.formName
        fields = self.analizeDataSpecList(createForm.dataSpecList)
        return Form(formName, *fields)
    
    def analizeDataSpecList(self, dataSpecList):
        dataSpecIterator = map(self.analizeDataSpec, dataSpecList)
        fields = list(dataSpecIterator)
        return fields
    
    def analizeDataSpec(self, dataSpec):
        className = getClassName(dataSpec)
        if className == "DataDefinition":
            return self.analizeDataDefinition(dataSpec)
        elif className == "DataReference":
            return self.analizeDataReference(dataSpec)
        
    def analizeDataDefinition(self, dataDefinition):
        dataName = dataDefinition.dataName
        dataType = dataDefinition.dataType
        notNull = dataDefinition.notNull
        unique = dataDefinition.unique
        return Field(dataName, dataType, notNull, unique)
    
    def analizeDataReference(self, dataReference):
        dataName = dataReference.dataName
        refCardinality = self.analizeRefCardinality(dataReference.refCardinality)
        refPath = self.analizeRefPath(dataReference.refPath)
        refConstraint = self.analizeRefConstraint(dataReference.refConstraint)
        return Reference(dataName, refCardinality, refPath, refConstraint)
    
    def analizeRefCardinality(self, refCardinality):
        cardinality1 = refCardinality.cardinality1
        cardinality2 = refCardinality.cardinality2
        return RefCardinality(cardinality1, cardinality2)
    
    def analizeRefPath(self, refPath):
        className = getClassName(refPath)
        if className == "SimpleId":
            return self.analizeSimpleId(refPath)
        elif className == "IdDotDataPath":
            return self.analizeIdDotDataPath(refPath)
        
    def analizeSimpleId(self, simpleId):
        return SimpleId(simpleId)
    
    def analizeIdDotDataPath(self, idDotDataPath):
        dataPath = []
        dataPath.append(SimpleId(idDotDataPath.id))
        dataPath.extend(self.analizeDataPath(idDotDataPath.dataPath))
        return DataPath(*dataPath)
    
    def analizeDataPath(self, dataPath):
        className = getClassName(dataPath)
        if className == "SimpleId":
            return self.analizeSimpleId(dataPath)
        elif className == "IdDotDataPath":
            return self.analizeIdDotDataPath(dataPath)
        elif className == "DataLabelList":
            return self.analizeDataLabelList(dataPath.dataLabelList)
        elif className == "All":
            return self.analizeAll(dataPath)
        
    def analizeDataLabelList(self, dataLabelList):
        dataLabels = list(map(self.analizeDataLabel, dataLabelList))
        return DataLabelList(*dataLabels)
    
    def analizeDataLabel(self, dataLabel):
        return DataLabel(dataLabel)
    
    def analizeAll(self, all):
        return All(all)
        
    def analizeRefConstraint(self, refConstraint):
        return RefConstraint(refConstraint)
    