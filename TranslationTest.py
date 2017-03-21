from SecretGoogleTranslationAPI import Translate

query = raw_input("Enter your text: ")
query = query.decode("utf-8")
obj = Translate()
print obj.translate(query)
