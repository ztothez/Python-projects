#Toni Tuunainen 1.3.3.6: Activity - Test the URL Request
import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
orig = "Washington"
dest = "Baltimaore"
key = "aULrPQsx1pNzm6Tn9dJJa9POwdmhXMUa"
url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest})

json_data = requests.get(url).json()
print(json_data)
