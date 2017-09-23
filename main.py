import subprocess
import os

mainPath = os.path.dirname(os.path.realpath(__file__)) + "/"

#list of all gpx files / activities
ridesList = os.listdir("activities/rides")
runsList = os.listdir("activities/runs")
hikesList = os.listdir("activities/hikes")

#merge gpx data TODO write code for runs and hikes
shellCommand = ["gpsbabel", "-i", "gpx"]

shellCommandRides = shellCommand
for file in ridesList:
    if file.endswith(".gpx"):
        shellCommandRides.extend(["-f", "activities/rides/"+file])

shellCommandRides.extend(["-o", "gpx", "-F", "activities/rides_merged.gpx"])
subprocess.call(shellCommandRides)

#run Maperitive script -> imports gpx files into Maperitive and render them end export as map-tiles
subprocess.call("./runMaperitive.sh")




