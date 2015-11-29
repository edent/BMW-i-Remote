#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Quentin's refactoring of Terence's original tweeting code
#
# This keeps a timestamp in tweet_status.json - you can 
# create it initially by copying the included sample file.

import bmw
import json
from dateutil import parser
import sys

# Connect to the server
c = bmw.ConnectedDrive()

#	Get the VIN
vehicle_json = c.call("/user/vehicles/")
vin = vehicle_json["vehicles"][0]["vin"]

#	Details about last trip
trip_url = "/user/vehicles/"+vin+"/statistics/lastTrip"
trip_json = c.call(trip_url)
distance  = bmw.KM_TO_MILES * trip_json["lastTrip"]["totalDistance"]
duration  = trip_json["lastTrip"]["duration"]
elec      = 1/(bmw.EFFICIENCY * trip_json["lastTrip"]["avgElectricConsumption"])

#	Vehicle Status
status_url  = "/user/vehicles/"+vin+"/status"
status_json = c.call(status_url)["vehicleStatus"]
battery          = status_json["chargingLevelHv"]
electricMiles    = status_json["remainingRangeElectricMls"]
mileage          = status_json["mileage"] * bmw.KM_TO_MILES
connectionStatus = status_json["connectionStatus"]
chargingStatus   = status_json["chargingStatus"]
updateTime       = status_json["updateTime"]
updateReason     = status_json["updateReason"]

# When did we last post?
with open("tweet_status.json", "r") as fp:
	tweet_status = json.load(fp)
oldUpdateTime = tweet_status["updateTime"]

# If nothing updated since previous tweet, exit here
if ( parser.parse(updateTime) <= parser.parse(oldUpdateTime) ):
	sys.exit(0)

tweet_status["updateTime"] = updateTime
with open("tweet_status.json", "w") as fp:
	json.dump(tweet_status, fp, indent=4)

#	Human readable text based on status
CHARGING_TRANSLATIONS = {
	"CHARGING" :               "Charging",
	"ERROR" :                  "Error",
	"FINISHED_FULLY_CHARGED" : "Finished (Full)",
	"FINISHED_NOT_FULL" :      "Finished (Partial)",
	"INVALID" :                "Invalid",
	"NOT_CHARGING" :           "Not charging",
	"WAITING_FOR_CHARGING" :   "Waiting for charge",
}

if connectionStatus == "DISCONNECTED" :
	chargingText ="Unplugged"
else:
	chargingText = CHARGING_TRANSLATIONS.get(chargingStatus, "Unknown")

UPDATE_TRANSLATIONS = {
   "CHARGING_INTERRUPED" :            "Charging Interrupted ",
   "CHARGING_PAUSED" :                "Charging Paused",
   "CHARGIN_STARTED" :                "Charging started",
   "CYCLIC_RECHARGING" :              "Cyclic Recharging",
   "DOOR_STATE_CHANGED" :             "Doors changed",
   "NO_CYCLIC_RECHARGING" :           "No Cyclic Recharging",
   "NO_LSC_TRIGGER" :                 "No LSC Trigger",
   "ON_DEMAND" :                      "Charging On Demand",
   "PREDICTION_UPDATE" :              "Prediction Update",
   "TEMPORARY_POWER_SUPPLY_FAILURE" : "Temporary Power Supply Failure",
   "UNKNOWN" :                        "???",
   "VEHICLE_MOVING" :                 "On the move",
   "VEHICLE_SECURED" :                "Locked",
   "VEHICLE_SHUTDOWN" :               "Shutdown",
   "VEHICLE_SHUTDOWN_SECURED" :       "Shutdown Secured",
   "VEHICLE_UNSECURED" :              "Unlocked",
}
updateText = UPDATE_TRANSLATIONS.get(updateReason, "???")


#	Generate the Tweet

# 🚗 37 miles in 70 minutes
# Efficiency: 4.03 miles/kWh
# 🔋 58% (45 miles)
# 🔌 Unplugged
# ⚠: Shutdown Secured
# 2,156 miles total

tweet  = u"🚗 " + "{:,.0f}".format(round(distance,2)) + " miles in " + str(duration)  + " minutes"
tweet += u"\nEfficiency: " + str("%.2f" % round(elec,2)) + " miles/kWh"
tweet += u"\n🔋 " + str(battery) + "% (" + str("%.0f" % round(electricMiles)) + " miles)"
tweet += u"\n🔌 " + chargingText
tweet += u"\n⚠ " + updateText
tweet += u"\n" + "{:,.0f}".format(round(mileage,2)) + " miles total"

# twitter.update_status(tweet)
print "Would tweet:"
print tweet
