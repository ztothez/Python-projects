#1.3.3.12: Activity - Test Quit Functionality
import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
while True:
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        break
    dest = input("Destination: ")
    if dest == "quit" or dest == "q":
        break
    key = "aULrPQsx1pNzm6Tn9dJJa9POwdmhXMUa"
    url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest})
    print("URL: " + (url))
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]
