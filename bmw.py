#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib, urllib, json, tweepy, time

#https://pypi.python.org/pypi/python-dateutil
from dateutil import parser

#	API Gateway
host     = "b2vapi.bmwgroup.com"

#	Constants
kmToMiles  = 0.621371
efficiency = 0.01609344

def generateCredentials():
	#	API Credentials loaded from credentials.json
	username = credentials["username"]
	password = credentials["password"]
	Authorization_Basic = credentials["Authorization_Basic"]

	#	OAuth
	oauth_url = "/webapi/oauth/token/"

	#	Manually enter URL Encoded email address. Password may not need to be encoded.
	params = "grant_type=password&username="+username+"&password="+password+"&scope=remote_services+vehicle_data"

	headers = {"Authorization": "Basic " + Authorization_Basic, 
			   "Content-Type": "application/x-www-form-urlencoded",
			   "User-Agent":"Dalvik/2.1.0 (Linux; U; Android 5.1.1; Nexus 6 Build/LMY48Y)"}

	#	Connect to the API
	conn = httplib.HTTPSConnection(host)

	#	Post the data
	conn.request("POST", oauth_url, params, headers)
	response = conn.getresponse()

	#	Did this succeed?
	#print response.status, response.reason

	#	Get the JSON
	data = response.read()
	conn.close()

	#	Parse the JSON
	json_data = json.loads(data)

	#	Get the access token
	access_token = json_data["access_token"]
	expires_in   = json_data["expires_in"]

	credentials["time"]         = time.time() + expires_in,
	credentials["access_token"] =  access_token
	
	saveCredentials()

	#	And done...
	return access_token

def saveCredentials():
	# Open a file for writing
	credentials_file = open("credentials.json","w")

	# Save the dictionary into this file
	# (the 'indent=' is optional, but makes it more readable)
	json.dump(credentials, credentials_file, indent=4)                                    

	# Close the file
	credentials_file.close()


def apiCall(path):
	headers = {"Authorization": "Bearer " + access_token, 
			   "User-Agent":"Dalvik/2.1.0 (Linux; U; Android 5.1.1; Nexus 6 Build/LMY48Y)"}
	#	Connect to the API
	conn = httplib.HTTPSConnection(host)

	#	Get the data
	conn.request("GET", path, "", headers)
	response = conn.getresponse()

	#	Did this succeed?
	#print response.status, response.reason

	#	Get the JSON
	data = response.read()
	conn.close()

	api_json = json.loads(data)

	return api_json

#   Load Credentials
in_file = open("credentials.json","r")
credentials = json.load(in_file)
in_file.close()

#	If the access_token has expired, generate a new one and use that
if (time.time() >= credentials["time"]):
	access_token = generateCredentials()
else:
	access_token = credentials["access_token"]

#	Get the VIN
vehicle_info_url = "/webapi/v1/user/vehicles/"
vehicle_json = apiCall(vehicle_info_url)
vin = vehicle_json["vehicles"][0]["vin"]

#	Details about last trip
trip_url = "/webapi/v1/user/vehicles/"+vin+"/statistics/lastTrip"
trip_json = apiCall(trip_url)
distance  = kmToMiles * trip_json["lastTrip"]["totalDistance"]
duration  = trip_json["lastTrip"]["duration"]
elec      = 1/(efficiency * trip_json["lastTrip"]["avgElectricConsumption"])

#	Vehicle Status
status_url  = "/webapi/v1/user/vehicles/"+vin+"/status"
status_json = apiCall(status_url)
battery          = status_json["vehicleStatus"]["chargingLevelHv"]
electricMiles    = status_json["vehicleStatus"]["remainingRangeElectricMls"]
mileage          = status_json["vehicleStatus"]["mileage"] * kmToMiles
connectionStatus = status_json["vehicleStatus"]["connectionStatus"]
chargingStatus   = status_json["vehicleStatus"]["chargingStatus"]
updateTime       = status_json["vehicleStatus"]["updateTime"]
updateReason     = status_json["vehicleStatus"]["updateReason"]

oldUpdateTime = credentials["updateTime"]

#	If the updateTime is newer than previously, 
#	Update the credentials file and send a tweet
if ( parser.parse(oldUpdateTime) < parser.parse(updateTime) ):
	credentials["updateTime"] = updateTime
	saveCredentials()

	#	Human readable text based on status
	if connectionStatus == "DISCONNECTED" :
		chargingText ="Unplugged"
	elif chargingStatus == "CHARGING" :
		chargingText = "Charging"
	elif chargingStatus =="ERROR":
		chargingText = "Error"
	elif chargingStatus =="FINISHED_FULLY_CHARGED":
		chargingText = "Finished (Full)"
	elif chargingStatus =="FINISHED_NOT_FULL":
		chargingText = "Finished (Partial)"
	elif chargingStatus =="INVALID":
		chargingText = "Invalid"
	elif chargingStatus =="NOT_CHARGING":
		chargingText = "Not charging"
	elif chargingStatus =="WAITING_FOR_CHARGING":
		chargingText = "Waiting for charge"
	else:
		chargingText ="Unknown"

	if updateReason == "CHARGING_INTERRUPED" :
		updateText ="Charging Interrupted "
	elif updateReason == "CHARGING_PAUSED" :
		updateText ="Charging Paused"
	elif updateReason == "CHARGIN_STARTED" :
		updateText ="Charging started"
	elif updateReason == "CYCLIC_RECHARGING" :
		updateText ="Cyclic Recharging"
	elif updateReason == "DOOR_STATE_CHANGED" :
		updateText ="Doors changed"
	elif updateReason == "NO_CYCLIC_RECHARGING" :
		updateText ="No Cyclic Recharging"
	elif updateReason == "NO_LSC_TRIGGER" :
		updateText ="No LSC Trigger"
	elif updateReason == "ON_DEMAND" :
		updateText ="Charging On Demand"
	elif updateReason == "PREDICTION_UPDATE" :
		updateText ="Prediction Update"
	elif updateReason == "TEMPORARY_POWER_SUPPLY_FAILURE" :
		updateText ="Temporary Power Supply Failure"
	elif updateReason == "UNKNOWN" :
		updateText ="???"
	elif updateReason == "VEHICLE_MOVING" :
		updateText ="On the move"
	elif updateReason == "VEHICLE_SECURED" :
		updateText ="Locked"
	elif updateReason == "VEHICLE_SHUTDOWN" :
		updateText ="Shutdown"
	elif updateReason == "VEHICLE_SHUTDOWN_SECURED" :
		updateText ="Shutdown Secured"
	elif updateReason == "VEHICLE_UNSECURED" :
		updateText ="Unlocked"
	else:
		updateText ="???"

	#   Set Up Twitter
	access_token        = credentials["access_token"]
	access_token_secret = credentials["access_token_secret"]
	consumer_key        = credentials["consumer_key"]
	consumer_secret     = credentials["consumer_secret"]
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	twitter = tweepy.API(auth)

	#	Generate the Tweet

	# 🚗 37 miles in 70 minutes
	# Efficiency: 4.03 miles/kWh
	# 🔋 58% (45 miles)
	# 🔌 Unplugged
	# ⚠: Shutdown Secured
	# 2,156 miles total
	
	tweet  = u"🚗 " + "{:,.0f}".format(round(distance,2)) + " miles in " + str(duration)  + " minutes"
	tweet += u"\nEfficiency: " +str("%.2f" % round(elec,2))  + " miles/kWh"
	tweet += u"\n🔋 " + str(battery) + "% (" + str("%.0f" % round(electricMiles)) + " miles)"
	tweet += u"\n🔌 " + chargingText
	tweet += u"\n⚠: " + updateText
	tweet += u"\n" + "{:,.0f}".format(round(mileage,2)) + " miles total"

	twitter.update_status(tweet)
	# print tweet