#1.3.3.8: Activity - Test Status and URL Print Commands

import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
orig = "Washington"
dest = "Baltimaore"
key = "aULrPQsx1pNzm6Tn9dJJa9POwdmhXMUa"
url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest})

print("URL: " + (url))

json_data = requests.get(url).json()
json_status = json_data["info"]["statuscode"]

if json_status == 0:
    print("API Status: " + str(json_status) + " = A successful route call.\n")
