from fqllang.core import getPostgreCodeFromFqlCode

postgreCode1 = getPostgreCodeFromFqlCode("create form Person (name TEXT, age NUMBER)")
postgreCode2 = getPostgreCodeFromFqlCode("get Person")
postgreCode3 = getPostgreCodeFromFqlCode("get Person with name='Leandro'")
postgreCode4 = getPostgreCodeFromFqlCode("get Person with name='Leandro' and age=20")

print(postgreCode1)
print(postgreCode2)
print(postgreCode3)
print(postgreCode4)
