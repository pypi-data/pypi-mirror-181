"""Testing nazca4sdk """

from nazca4sdk.sdk import SDK

sdk = SDK(False)

result = sdk.write_cache_keys("franek", 2147483647)
print(result)
result = sdk.read_cache_keys(['franek', "gruby:p4"])
print(result)
