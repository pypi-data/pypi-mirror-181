

from dsl.fql.base import Fql
from dsl.utils import getClassName

class Form:
    def __init__(self, name, *fields) -> None:
        self.name = name
        self.fields = fields
        
    def generate(self):
        return CreateForm(self.name, *self.fields).generate()
    
    def __str__(self):
        return self.generate()
    
class FormList:
    def __init__(self, *forms) -> None:
        self.forms = forms
        
    def __iter__(self):
        for form in self.forms:
            yield form
            
    def generate(self):
        strGenerated = map(lambda form: form.generate(), self)
        return "\n".join(strGenerated)
    
    def __str__(self) -> str:
        return self.generate()


class CreateForm(Fql):
    def __init__(self, formName, *dataSpecs) -> None:
        self.formName = formName
        self.dataSpecs = dataSpecs


class DataSpec(Fql):
    def __init__(self, dataName) -> None:
        self.dataName = dataName


class DataDefinition(DataSpec):
    def __init__(self, dataName, dataType, primaryKey=None, notNull=None, unique=None) -> None:
        super().__init__(dataName)
        self.dataType = dataType
        self.notNull = notNull
        self.unique = unique
        self.primaryKey = primaryKey


class DataReference(DataSpec):
    def __init__(self, dataName, refPath, refCardinality=None) -> None:
        super().__init__(dataName)
        self.refPath = refPath
        self.refCardinality = refCardinality


class RefCardinality(Fql):
    def __init__(self, cardinality1, cardinality2=None) -> None:
        super().__init__()
        self.cardinality1 = cardinality1
        self.cardinality2 = cardinality2
