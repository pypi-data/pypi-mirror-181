from nazca4sdk import SDK
from nazca4sdk import UserVariable, UserVariableInfo, UserVariableDataType

u = UserVariable("SZMATA", "Jebaj", 13.2)
u1 = UserVariable(UserVariableDataType.DOUBLE, "ostro", 43.1)
u2 = UserVariable(UserVariableDataType.INT, "ostro", 127)
u3 = UserVariable(UserVariableDataType.BOOL, "ostro", True)
u4 = UserVariable(UserVariableDataType.BOOL, "ostro", False)
u7 = UserVariable(UserVariableDataType.INT, "ostro", 236)
u5 = UserVariable(UserVariableDataType.TEXT, "ostro", "Nie lubisz?")
u6 = UserVariable(UserVariableDataType.TEXT, "ostro", "Nie lubie!")
ud = UserVariable(UserVariableDataType.DATETIME, "ostro", "2022-10-04T15:05:01")

sdk = SDK(False)
print(sdk.write_hotstorage_variables([u, u1, u2, u3, u4, u5, u6, ud]))
#
va = UserVariableInfo(name="ostro", type=UserVariableDataType.INT)
va2 = UserVariableInfo(name="ostro", type="anal")
res = sdk.read_hotstorage_variables("2022-10-04T00:40:02", "2022-10-05T17:00:00", [va, va2])
# print(len(res))
# for x in res:
#     print(x)
