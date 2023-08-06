"""Testing nazca4sdk """

from nazca4sdk.file_storage import FileStorage

# sdk = SDK()
# print(sdk.modules)

fs = FileStorage(True)
file = fs.download_file("/siemka.txt", "./Dupa.txt")
# fs.send_file('/Sodomita.txt', "./Korek.txt")
print("OK")
