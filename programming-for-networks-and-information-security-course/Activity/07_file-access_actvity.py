#Toni Tuunainen 1.2.6.4: Activity – Create a Script to Allow User to Add Devices
devices=[]
file=open("devices.txt","a")
while True:
    newItem=input("Enter device name: ")
    if newItem == 'exit' :
        file.close()
        print("All done!")
        break
    while True:
        file.write(newItem + "\n")
        break
