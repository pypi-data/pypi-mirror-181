
class Fql:
    pass


class Field:
    def __init__(self, name, dataType, *dataConstraints) -> None:
        self.name = name
        self.dataType = dataType
        self.dataConstraints = dataConstraints


class Reference:
    def __init__(self, dataName, refCardinality, refPath, refConstraint) -> None:
        self.dataName = dataName
        self.refCardinality = refCardinality
        self.refPath = refPath
        self.refConstraint = refConstraint


class RefCardinality:
    def __init__(self, cardinality1, cardinality2) -> None:
        self.cardinality1 = cardinality1
        self.cardinality2 = cardinality2


class RefConstraint:
    def __init__(self, constraint) -> None:
        self.constraint = constraint


class SimpleId:
    def __init__(self, id) -> None:
        self.id = id


class DataPath:
    def __init__(self, *dataPath) -> None:
        self.path = dataPath

    def __iter__(self):
        for data in self.dataPath:
            yield data


class DataLabelList:
    def __init__(self, *dataLabels) -> None:
        self.dataLabels = dataLabels


class DataLabel(SimpleId):
    def __init__(self, id) -> None:
        super().__init__(id)


class All:
    def __init__(self, all) -> None:
        self.star = all
