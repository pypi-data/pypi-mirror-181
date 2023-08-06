from nazca4sdk.datahandling.knowledge.knowledge_data_type import KnowledgeDataType
from nazca4sdk.sdk import SDK

sdk = SDK(False)
# odczyt dla danego klucza
# values = sdk.read_knowledge("blob")
# print(values)

# result = sdk.write_knowledge("blob", "pliczek", "/2022-07-07_14-31.png", KnowledgeDataType.BLOB)
result = sdk.write_knowledge("gruby", "sekcjaGruby", "test", KnowledgeDataType.TEXT)
print(result)
