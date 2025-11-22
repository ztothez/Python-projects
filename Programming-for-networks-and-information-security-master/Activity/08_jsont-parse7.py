#1.3.3.19: Activity - Test Full Application Functionality
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
    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n"
        + ("Directions from " + (orig) + " to " + (dest)+ "\nTrip Duration:   " + str(json_data["route"]["formattedTime"])
       + "\n Kilometers:      " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)
        + "\nFuel Used (Ltr): " +
        str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)+"\n============================================="))))
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))
        print("=============================================\n")
    elif json_status == 402:
        print("\n****************************************************************")
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("****************************************************************\n")
    else:
        print("\n************************************************************************")
        print("Status Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************************************************************\n")
