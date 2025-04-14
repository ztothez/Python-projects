#Toni Tuunainen 1.3.4.3: Option 3 - Create an App for the ISS normal

import json, urllib.request, time

#people in space
url = "http://api.open-notify.org/astros.json"
response = urllib.request.urlopen(url)
result = json.loads(response.read())
people = result["people"]
print("People in Space: " ,result["number"],"\n")
for p in people:
  print(p["name"],p["craft"])

#where is iss
url = "http://api.open-notify.org/iss-now.json"
response = urllib.request.urlopen(url)
result = json.loads(response.read())
location = result["iss_position"]
isslat = float(location["latitude"])
isslon = float(location["longitude"])
print("Iss is at: ",isslat," ",isslon)

print("\nDuration means pass lenght in seconds")

#Passed today
url = "http://api.open-notify.org/iss-pass.json"
url = url + "?lat=" +str(isslat) + "&lon=" + str(isslon)
response = urllib.request.urlopen(url)
result = json.loads(response.read())
times = result["request"]["passes"]
duration = result["response"]
print("\nPasses for today: ",times,"\n")

for d in duration:
  print("The duration is: ",d["duration"],"\nThe risetime is: ",time.ctime(d["risetime"]))

#overheard on location
url = "http://api.open-notify.org/iss-pass.json"
url = url + "?lat=" +str(isslat) + "&lon=" + str(isslon)
response = urllib.request.urlopen(url)
result = json.loads(response.read())
over = result["response"][1]["risetime"]
readable = time.ctime(over)
print("\nISS next time on: "+readable)

#Turku
mylat = 60.4518
mylon = 22.2666

#Passed today
url = "http://api.open-notify.org/iss-pass.json"
url = url + "?lat=" +str(mylat) + "&lon=" + str(mylon)
response = urllib.request.urlopen(url)
result = json.loads(response.read())
times = result["request"]["passes"]
duration = result["response"]
print("\nPasses for today: ",times,"\n")

for d in duration:
  print("The duration is: ",d["duration"],"\nThe risetime is: ",time.ctime(d["risetime"]))

#overheard on location
url = "http://api.open-notify.org/iss-pass.json"
url = url + "?lat=" +str(mylat) + "&lon=" + str(mylon)
response = urllib.request.urlopen(url)
result = json.loads(response.read())
over = result["response"][1]["risetime"]
readable = time.ctime(over)
print("\nSeen next time on Turku: "+readable)
