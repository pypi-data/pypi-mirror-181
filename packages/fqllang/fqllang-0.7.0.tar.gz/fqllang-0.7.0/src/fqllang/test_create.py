
from modules.fqlAstBuilder.ast import FqlAstBuilder
from modules.fqlBuilder.modelAnalizer import ModelAnalizer

def model_from_code(code):
    model = FqlAstBuilder.fqlAstFromCode(code)
    ast = ModelAnalizer(model).analizeModel()
    return ast

code = "create form Person(Project references Projects)"
model_from_code(code)
code = "create form Person(Project references 1 Projects)"
model_from_code(code)
code = "create form Person(Project references 0..1 Projects)"
model_from_code(code)
code = "create form Person(Project references 0..many Projects)"
model_from_code(code)
code = "create form Person(Project references 0..many Projects.*)"
model_from_code(code)
code = "create form Person(Project references 0..many Projects.Animal.*)"
model_from_code(code)
code = "create form Person(Project references 0..many Projects.Animal.(name, age) UNIQUE)"
model_from_code(code)
code = "create form Person(Project references 0..many Projects.Animal.(name, age) TOTALLY UNIQUE)"
model_from_code(code)


