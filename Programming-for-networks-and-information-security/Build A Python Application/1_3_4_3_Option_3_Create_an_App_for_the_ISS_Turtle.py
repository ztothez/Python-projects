#1.3.4.3: Option 3 - Create an App for the ISS Turtle-Edition

import json, turtle, urllib.request, time

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
lat = float(location["latitude"])
lon = float(location["longitude"])
print("\nlatitude: ",repr(lat), "\nLongitude: ",repr(lon))

#Passed today
url = "http://api.open-notify.org/iss-pass.json"
url = url + "?lat=" +str(lat) + "&lon=" + str(lon)
response = urllib.request.urlopen(url)
result = json.loads(response.read())
times = result["request"]["passes"]
duration = result["response"]
print("\nPasses for today: ",times,"\n")

for d in duration:
  print("The duration is: ",d["duration"],"\nThe risetime is: ",time.ctime(d["risetime"]))

#turtle map
screen = turtle.Screen()
screen.setup(720, 360)
screen.setworldcoordinates(-180,-90,180,90)
screen.bgpic("map.gif")

screen.register_shape("iss.gif")
iss = turtle.Turtle()
iss.shape("iss.gif")
iss.setheading(90)

iss.penup()
iss.goto(lon, lat)

#iss overheard
iss.penup()
iss.goto(lon, lat)

#Turku
lat = 60.4518
lon = 22.2666
location = turtle.Turtle()
location.penup()
location.color("yellow")
location.goto(lon,lat)
location.dot(5)
location.hideturtle()

#overheard on location
url = "http://api.open-notify.org/iss-pass.json"
url = url + "?lat=" +str(lat) + "&lon=" + str(lon)
response = urllib.request.urlopen(url)
result = json.loads(response.read())
over = result["response"][1]["risetime"]
style = ("arial",6,"bold")
location.write(time.ctime(over), font=style)
