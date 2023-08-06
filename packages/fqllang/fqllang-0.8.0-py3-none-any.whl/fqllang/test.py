from core import getPostgreCodeFromFqlCode

postgreCode1 = getPostgreCodeFromFqlCode("create form Person(name TEXT, age NUMBER)")
postgreCode2 = getPostgreCodeFromFqlCode("create form Person(name TEXT, age NUMBER, Product references Products)")

postgreCode3 = getPostgreCodeFromFqlCode("create new Person (name='Leandro', age=23, isCold=True)")

postgreCode4 = getPostgreCodeFromFqlCode("get Person")
postgreCode5 = getPostgreCodeFromFqlCode("get Person with name='Leandro'")
postgreCode6 = getPostgreCodeFromFqlCode("get Person with name='Leandro' and age=23")




print(postgreCode1)
print(postgreCode2)
print()
print(postgreCode3)
print()
print(postgreCode4)
print(postgreCode5)
print(postgreCode6)