from nazca4sdk.sdk import SDK

sdk = SDK(False)

print(sdk.modules)

print(sdk.variables)

# # df = sdk.variable_over_time('BCM', ['vRmsy'], 10, 'MINUTE')
# # df = sdk.variable_over_time('symulator', ['V1'], 3, 'HOUR')
# df = sdk.variable_over_day("symulator", ["Q2"], "2022-10-18T07:34:41", "2022-10-18T09:00:00")
# # df = sdk.variable_over_time("symulator", ["Q2"], 3, "HOUR")
# print(df)
