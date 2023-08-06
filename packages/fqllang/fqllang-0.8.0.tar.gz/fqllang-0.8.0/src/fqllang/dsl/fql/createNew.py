
from dsl.fql.base import Fql


class CreateNew(Fql):
    def __init__(self, formName, *newValues) -> None:
        super().__init__()
        self.formName = formName
        self.newValues = newValues
        
class CreateNewValues(Fql):
    def __init__(self, keys, values) -> None:
        super().__init__()
        self.keys = keys
        self.values = values
    
    @staticmethod
    def createNewValuesFromValueList(*values):
        return CreateNewValues(None,*values)
        