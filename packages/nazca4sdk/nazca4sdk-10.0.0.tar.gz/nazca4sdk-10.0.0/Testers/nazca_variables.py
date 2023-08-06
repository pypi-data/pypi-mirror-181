from nazca4sdk import SDK

sdk = SDK(False)
print(sdk.read_nazca_variables())

value = sdk.read_nazca_variable("grubyDouble")
print(value)
