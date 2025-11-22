import pgeocode
#import json
country = input("Add country code: ")
postalcode = input("Add postalcode: ")
nomi = pgeocode.Nominatim(country)
lists = nomi.query_postal_code(postalcode).tolist()
#js = json.dumps(lists)
print(lists)



