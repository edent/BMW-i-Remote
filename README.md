# BMW i Remote API
A reverse engineered interface for the BMW i3 Electric Car, created initially by Terence Eden, with some code modified by Quentin Stafford-Fraser.

[![Buy me a coffee](https://www.ko-fi.com/img/donate_sm.png)](https://ko-fi.com/edent)

## Description
These API calls are designed to allow you to interact with your BMW i3.  They were reverse engineered from [the official BMW i Remote Android app](https://play.google.com/store/apps/details?id=com.bmwi.remote).

Your use of these API calls is entirely at your own risk.  They are neither officially provided nor sanctioned.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

- [Servers](#servers)
- [Authorisation](#authorisation)
- [API](#api)
	- [Get Vehicle Data](#get-vehicle-data)
		- [Response](#response)
		- [Values](#values)
	- [Get Last Trip](#get-last-trip)
		- [Response](#response)
		- [Values](#values)
	- [Get Charging Times](#get-charging-times)
		- [Response](#response)
		- [Values](#values)
	- [Get Vehicle Destinations](#get-vehicle-destinations)
		- [Response](#response)
		- [Values](#values)
	- [Get All Trip Details](#get-all-trip-details)
		- [Response](#response)
		- [Values](#values)
	- [Get Range Map](#get-range-map)
		- [Response](#response)
		- [Values](#values)
	- [Get misc SoC data](#get-misc-soc-data)
		- [Response](#response)
		- [Values](#values)	
- [Sending information to the car](#sending-information-to-the-car)
	- [Get Request status](#get-request-status)
		- [Response](#response)
		- [Values](#values)
	- [POST a command](#post-a-command)
		- [Available Commands](#available-commands)
		- [Initiate Charging](#initiate-charging)
		- [Start Climate Control](#start-climate-control)
		- [Lock the doors](#lock-the-doors)
		- [Unlock the doors](#unlock-the-doors)
		- [Flash the headlights](#flash-the-headlights)
		- [Charging Schedule](#charging-schedule)
		- [Vehicle Finder](#vehicle-finder)
		- [Response](#response)
	- [Send POI](#send-poi)
		- [Body](#body)
		- [Response](#response)
- [What's Next?](#whats-next)

## Servers
There are three API servers.

* `https://b2vapi.bmwgroup.cn:8592` China
* `https://b2vapi.bmwgroup.us` USA
* `https://b2vapi.bmwgroup.com` Europe / Rest of World

## Authorisation
In order to authenticate against the API you will need to be registered on [BMW's Connected Drive service](https://www.bmw-connecteddrive.co.uk/cdp/release/internet/servlet/login?locale=en_GB).

You will need:

1. Your ConnectedDrive registered email address.
1. Your ConnectedDrive registered password.
1. The i Remote API Key.
1. The i Remote API Secret.

You can get the i Remote details from either decompiling the Android App or from intercepting communications between your phone and the BMW server.  This is left as an exercise for the reader ☺

Firstly, we use [Basic authentication](https://en.wikipedia.org/wiki/Basic_access_authentication).  That means taking the API Key and Secret and Base64 encoding them.

So `key:secret` becomes `a2V5OnNlY3JldA==`

We also need to send the following parameters as

* `Content-Type: application/x-www-form-urlencoded`

```
 grant_type=password
&username=whatever%40example.com
&password=p4ssw0rd
&scope=remote_services+vehicle_data
```

Here's how to do it with `curl`:

```
curl \
   -H "Authorization: Basic a2V5OnNlY3JldA==" \
   -H "Content-Type: application/x-www-form-urlencoded" \
   -d "grant_type=password&username=whatever%40example.com&password=p4ssw0rd&scope=remote_services+vehicle_data" \
   "https://b2vapi.bmwgroup.com/webapi/oauth/token/"
```

If everything has worked, you should get back the following JSON:

```
{
  "access_token": "RCQ1hLP4AFaUBW9BjcPUN3i4WgkwF90R",
  "token_type": "Bearer",
  "expires_in": 28800,
  "refresh_token": "7WgKmEJ2kD1ydl9Hefp01eS8qDGzKnzjeORpA6vtsoFIEanz",
  "scope": "vehicle_data remote_services"
}
```

You **must** include

* `Authorization: Bearer RCQ1hLP4AFaUBW9BjcPUN3i4WgkwF90R`

in your headers with *every* request.

The `expires_in` is in seconds - giving you 8 hours before you have to renew the token.

I've no idea what the `refresh_token` is for. Once the `access_token` expires, you can simply re-authenticate and gain a new one.

## API
You **must** include

* `Authorization: Bearer RCQ1hLP4AFaUBW9BjcPUN3i4WgkwF90R`

in your headers with *every* request.

### Get Vehicle Data

* `/webapi/v1/user/vehicles/`
    * Remember to include the `Authorization: Bearer` header.

#### Response

Returns a list of entries, one per registered vehicle.
```
[
  {
    "remote360": "NOT_SUPPORTED",
    "chargingControl": "WEEKLY_PLANNER",
    "countryCode": "V1-UK",
    "hornBlow": "NOT_SUPPORTED",
    "brand": "BMW_I",
    "smartSolution": "NOT_SUPPORTED",
    "hasAlarmSystem": true,
    "climateControl": "NOT_SUPPORTED",
    "doorUnlock": "ACTIVATED",
    "rangeMap": "RANGE_POLYGON",
    "climateFunction": "AIRCONDITIONING",
    "lscType": "I_LSC_IMM",
    "hub": "HUB_ECE",
    "statisticsAvailable": true,
    "doorLock": "ACTIVATED",
    "intermodalRouting": "AVAILABLE",
    "model": "I3 +REX",
    "vehicleFinder": "ACTIVATED",
    "color": "SOLARORANGE MET. M. AKZE",
    "vin": "WAB1C23456V123456",
    "bodytype": "I01",
    "chargeNow": "NOT_SUPPORTED",
    "supportedChargingModes": [
      "AC_LOW",
      "AC_HIGH",
      "DC"
    ],
    "sendPoi": "ACTIVATED",
    "yearOfConstruction": 2014,
    "climateNow": "ACTIVATED",
    "lightFlash": "ACTIVATED",
    "driveTrain": "BEV_REX",
    "licensePlate": "AB64 1BC",
    "statisticsCommunityEnabled": true,
    "colorCode": "B78",
    "onlineSearchMode": "MAP",
    "dealer": {
      "name": "BMW UK Ltd",
      "country": "GB",
      "postalCode": "GU14 0FB",
      "city": "Farnborough",
      "street": "Summit ONE"
    },
    "lastDestinations": "SUPPORTED"
  }
]
```

The most important thing here is the VIN - Vehicle Identification Number.  You'll need that for all the other API calls <strong>as well as the</strong> Authorization Bearer.

### Get Vehicle Status

* `/webapi/v1/user/vehicles/:VIN/status`
    * Where `:VIN` is your vehicle's VIN.
    * Remember to include the `Authorization: Bearer` header.

#### Response
```
{
    "vehicleStatus": {
        "vin": "WAB1C23456V123456",
        "mileage": 1234,
        "updateReason": "VEHICLE_SHUTDOWN_SECURED",
        "updateTime": "2015-10-30T18:45:04+0100",
        "doorDriverFront": "CLOSED",
        "doorDriverRear": "CLOSED",
        "doorPassengerFront": "CLOSED",
        "doorPassengerRear": "CLOSED",
        "windowDriverFront": "CLOSED",
        "windowDriverRear": "CLOSED",
        "windowPassengerFront": "CLOSED",
        "windowPassengerRear": "CLOSED",
        "trunk": "CLOSED",
        "rearWindow": "INVALID",
        "convertibleRoofState": "INVALID",
        "hood": "CLOSED",
        "doorLockState": "SECURED",
        "parkingLight": "OFF",
        "positionLight": "OFF",
        "remainingFuel": 8.9,
        "remainingRangeElectric": 73,
        "remainingRangeElectricMls": 45,
        "remainingRangeFuel": 126,
        "remainingRangeFuelMls": 78,
        "maxRangeElectric": 134,
        "maxRangeElectricMls": 83,
        "fuelPercent": 99,
        "maxFuel": 9,
        "connectionStatus": "DISCONNECTED",
        "chargingStatus": "INVALID",
        "chargingLevelHv": 58,
        "lastChargingEndReason": "UNKNOWN",
        "lastChargingEndResult": "FAILED",
        "position": {
            "lat": 51.123456,
            "lon": -1.2345678,
            "heading": 211,
            "status": "OK"
        },
        "chargingTimeRemaining": 45,
        "internalDataTimeUTC": "2015-10-30T18:47:44"
    }
}
```

#### Values
* `mileage` is in **Km**.
* `remainingFuel` is in Litres.
* `maxRangeElectric` is in Km.
* `maxRangeElectricMls` is in miles.
* `chargingLevelHv` is the percentage of charge left in the (**H**igh **v**oltage?) battery.
* `maxFuel` is in Litres.
* `heading` is in degrees.
* `chargingTimeRemaining` is in minutes. Please mind that this value is _only_ available if car is actively charging otherwise it is _not_ present in the response.

Valid `chargingStatus` values appear to be:

* `CHARGING`
* `ERROR`
* `FINISHED_FULLY_CHARGED`
* `FINISHED_NOT_FULL`
* `INVALID`
* `NOT_CHARGING`
* `WAITING_FOR_CHARGING`

Valid `connectionStatus` values appear to be:

* `CHARGING_DONE`
* `CHARGING_INTERRUPED` [sic]
* `CHARGING_PAUSED`
* `CHARGIN_STARTED` [sic] **TYPO** should be `CHARGING_STARTED`
* `CYCLIC_RECHARGING`
* `DISCONNECTED`
* `DOOR_STATE_CHANGED`
* `NO_CYCLIC_RECHARGING`
* `NO_LSC_TRIGGER`
* `ON_DEMAND`
* `PREDICTION_UPDATE`
* `TEMPORARY_POWER_SUPPLY_FAILURE`
* `UNKNOWN`
* `VEHICLE_MOVING`
* `VEHICLE_SECURED`
* `VEHICLE_SHUTDOWN`
* `VEHICLE_SHUTDOWN_SECURED`
* `VEHICLE_UNSECURED`

Valid `doorLockState` values appear to be:

* `UNLOCKED`
* `LOCKED`  (remotely)
* `SECURED` (with key fob)

### Get Last Trip
Shows the details about your most recent trip.

* `/webapi/v1/user/vehicles/:VIN/statistics/lastTrip`
    * Where `:VIN` is your vehicle's VIN.
    * Remember to include the `Authorization: Bearer` header.

#### Response
```
{
   "lastTrip":{
      "efficiencyValue":0.53,
      "totalDistance":141,
      "electricDistance":100.1,
      "avgElectricConsumption":16.6,
      "avgRecuperation":2,
      "drivingModeValue":0,
      "accelerationValue":0.39,
      "anticipationValue":0.81,
      "totalConsumptionValue":0.79,
      "auxiliaryConsumptionValue":0.66,
      "avgCombinedConsumption":1.9,
      "electricDistanceRatio":71,
      "savedFuel":0,
      "date":"2015-12-01T20:44:00+0100",
      "duration":124
   }
}
```
#### Values

Distances appear to be in Kilometres rather than miles, so be sure to adjust accordingly. Multiply by `0.621371` to get miles.

* `totalDistance` is in Km.
* `electricDistance` is in Km.
* `avgElectricConsumption` is in kWh/100Km.
* `avgRecuperation` is in kWh/100Km.
* `duration` is in minutes.

To convert kWh/100Km to Miles/kWh.

`1 / (0.01609344 * avgElectricConsumption)`



### Get Charging Times
Shows when the car is scheduled to charge.

* `/webapi/v1/user/vehicles/:VIN/chargingprofile`
    * Where `:VIN` is your vehicle's VIN.
    * Remember to include the `Authorization: Bearer` header.

#### Response
```
{
   "weeklyPlanner":{
      "climatizationEnabled":true,
      "chargingMode":"DELAYED_CHARGING",
      "chargingPreferences":"CHARGING_WINDOW",
      "timer1":{
         "departureTime":"07:30",
         "timerEnabled":true,
         "weekdays":[
            "MONDAY"
         ]
      },
      "timer2":{
         "departureTime":"13:00",
         "timerEnabled":false,
         "weekdays":[
            "SATURDAY"
         ]
      },
      "timer3":{
         "departureTime":"08:00",
         "timerEnabled":false,
         "weekdays":[

         ]
      },
      "overrideTimer":{
         "departureTime":"07:30",
         "timerEnabled":false,
         "weekdays":[
            "MONDAY"
         ]
      },
      "preferredChargingWindow":{
         "enabled":true,
         "startTime":"05:02",
         "endTime":"17:31"
      }
   }
}
```
#### Values

* `departureTime` appears to be the car's local time.

### Get Vehicle Destinations
Shows the destinations you've previously sent to the car.

* `/webapi/v1/user/vehicles/:VIN/destinations`
    * Where `:VIN` is your vehicle's VIN.
    * Remember to include the `Authorization: Bearer` header.

#### Response
```
{
   "destinations":[
      {
         "lat":51.53053283691406,
         "lon":-0.08362331241369247,
         "country":"UNITED KINGDOM",
         "city":"LONDON",
         "street":"PITFIELD STREET",
         "type":"DESTINATION",
         "createdAt":"2015-09-25T08:06:11+0200"
      }
   ]
}
```
#### Values

* An array of locations.

### Get All Trip Details
Shows the statistics for all trips taken in the vehicle.

* `/webapi/v1/user/vehicles/:VIN/statistics/allTrips`
    * Where `:VIN` is your vehicle's VIN.
    * Remember to include the `Authorization: Bearer` header.

#### Response
```
{
    "allTrips": {
        "avgElectricConsumption": {
            "communityLow": 0,
            "communityAverage": 16.33,
            "communityHigh": 35.53,
            "userAverage": 14.76
        },
        "avgRecuperation": {
            "communityLow": 0,
            "communityAverage": 3.76,
            "communityHigh": 14.03,
            "userAverage": 2.3
        },
        "chargecycleRange": {
            "communityAverage": 121.58,
            "communityHigh": 200,
            "userAverage": 72.62,
            "userHigh": 135,
            "userCurrentChargeCycle": 60
        },
        "totalElectricDistance": {
            "communityLow": 1,
            "communityAverage": 12293.65,
            "communityHigh": 77533.6,
            "userTotal": 3158.66
        },
        "avgCombinedConsumption": {
            "communityLow": 0,
            "communityAverage": 1.21,
            "communityHigh": 6.2,
            "userAverage": 0.36
        },
        "batterySizeMax": 35820,
        "savedCO2": 87.58,
        "savedCO2greenEnergy": 515.177,
        "totalSavedFuel": 0,
        "resetDate": "1970-01-01T01:00:00+0100"
    }
}
```
#### Values

* `chargecycleRange` is in Km.
* `totalElectricDistance` is in Km.
* `savedCO2` is in kg.
* `savedCO2greenEnergy` is in kg.
* `batterySizeMax`is in Wh.

I'm not sure what units of the other values are.


### Get Range Map
Generate a polyline displaying the predicted range of the vehicle.

* `/webapi/v1/user/vehicles/:VIN/rangemap`
    * Where `:VIN` is your vehicle's VIN.
    * Remember to include the `Authorization: Bearer` header.

#### Response
```
{
    "rangemap": {
        "center": {
            "lat": 51.123456,
            "lon": -1.2345678
        },
        "quality": "AVERAGE",
        "rangemaps": [
            {
                "type": "ECO_PRO_PLUS",
                "polyline": [
                    {
                        "lat": 51.6991281509399,
                        "lon": -2.00423240661621
                    },
                    {
                        "lat": 51.6909098625183,
                        "lon": -1.91526889801025
                    },
                    ...
                ]
            },
            {
                "type": "COMFORT",
                "polyline": [
                    {
                        "lat": 51.7212295532227,
                        "lon": -1.7363977432251
                    },
                    {
                        "lat": 51.6991496086121,
                        "lon": -1.73077583312988
                    },
                    ...
                ]
            }
        ]
    }
}

```
#### Values

* `ECO_PRO_PLUS` driving using the efficient Eco mode.
* `COMFORT` driving using comfort mode.

### Get misc SoC Data
Get maximum state of charge of your battery and some redundant data.

The URL is different from the other API servers:
* `https://www.bmw-connecteddrive.de/api/vehicle/navigation/v1/VIN`
    * Where `VIN` is your vehicle's VIN.
    * Use the same `Authorization: Bearer` header as with API Server

#### Response
```
example data from a PHEV:
{
  "latitude" : 62.250584,
  "longitude" : 3.7717776,
  "isoCountryCode" : "DEU",
  "auxPowerRegular" : 1.4,
  "auxPowerEcoPro" : 1.2,
  "auxPowerEcoProPlus" : 0.4,
  "soc" : 4.019000053405762,
  "socMax" : 5.6,
  "eco" : "1c94,1206,d9d,d0f,cd3,cf9,e2d,f49,10ec,10ec,117c",
  "norm" : "1e15,12f9,e54,dbf,d82,da7,eed,1017,11d0,1483,19a9",
  "ecoEv" : "c31,799,5c5,5a5,5ae,5fc,6fb,861,9df,9df,9df",
  "normEv" : "cd5,800,613,5f1,5fc,64c,759,8d2,a65,bf8,e7d",
  "vehicleMass" : "1560",
  "kAccReg" : "1440000",
  "kDecReg" : "3420000",
  "kAccEco" : "1548000",
  "kDecEco" : "3240000",
  "kUp" : "1800000",
  "kDown" : "2700000",
  "driveTrain" : "phev_otto",
  "pendingUpdate" : false,
  "vehicleTracking" : true
}
```
#### Values

* `socMax` current maximum charge. kind of health check of you battery


## Sending information to the car
Sending information to the car is slightly complicated.

Your app communicates with the API, the API then communicates with the car's 3G modem, then you have to wait for a response.

If your car is in poor coverage, you can expect significant latency.  Often much higher than a typical timeout will allow for.

At a basic level, you can just send a request - for example to lock the doors, or set off-peak charging.


### Get Request status
Shows the status of a `POST`ed request

* `/webapi/v1/user/vehicles/:VIN/serviceExecutionStatus?serviceType=:SERVICE`
    * Where `:VIN` is your vehicle's VIN.
    * Remember to include the `Authorization: Bearer` header.

#### Response
```
{
   "executionStatus":{
      "serviceType":"DOOR_LOCK",
      "status":"EXECUTED",
      "eventId":"123456789012345AB1CD1234@bmw.de"
   }
}
```
#### Values
Valid `status`es are:

* `DELIVERED`
* `EXECUTED`
* `INITIATED`
* `NOT_EXECUTED`
* `PENDING`
* `TIMED_OUT`

The following are valid `:SERVICE` types, but **may not be supported by your vehicle**.

* `CHARGE_NOW`
* `CHARGING_CONTROL`
* `CLIMATE_CONTROL`
* `CLIMATE_NOW`
* `DOOR_LOCK`
* `DOOR_UNLOCK`
* `GET_ALL_IMAGES`
* `GET_PASSWORD_RESET_INFO`
* `GET_VEHICLES`
* `GET_VEHICLE_IMAGE`
* `GET_VEHICLE_STATUS`
* `HORN_BLOW`
	* This is disabled in the UK market.  It *may* be possible to [enable this by registering on the German ConnectedDrive service](https://speakev.com/threads/introducing-the-tweeting-i3.13177/#post-206168).
	* **NOTE** The [UK Highway Code says you may not use the horn *unless* moving (Rule 112)](https://www.gov.uk/guidance/the-highway-code/general-rules-techniques-and-advice-for-all-drivers-and-riders-103-to-158).
* `LIGHT_FLASH`
* `LOCAL_SEARCH`
* `LOCAL_SEARCH_SUGGESTIONS`
* `LOGIN`
* `LOGOUT`
* `SEND_POI_TO_CAR`
* `VEHICLE_FINDER`

### POST a command

Instructs the car to perform an action.

* `/webapi/v1/user/vehicles/:VIN/executeService`
    * Where `:VIN` is your vehicle's VIN.
    * Remember to include the `Authorization: Bearer` header.

#### Available Commands
These commands are all available via the API, but **may not be supported by your vehicle**.

These are just what I've discovered so far.

Data must be `POST`ed to the server.

#### Initiate Charging
If the vehicle is plugged in, but not charging (due to an off peak setting?) it is possible to force the car to charge.

* `serviceType=CHARGE_NOW`

#### Start Climate Control
This will activate climate control within your vehicle.

It *appears* to be limited to the last temperature you set when you were in the car. I can't find a way to instruct the car to reach a specific temperature.

* `serviceType=CLIMATE_NOW`

#### Lock the doors
Performs central locking.

* `serviceType=DOOR_LOCK`

#### Unlock the doors
This will unlock all the doors on your vehicle.

Please use **extreme caution** when sending this command.  Ensure that you are in sight of the vehicle and are able to lock it if needed.

* `serviceType=DOOR_UNLOCK`

If you recievce an error after DOOR_UNLOCK that looks like 
```{"error":{"code":500,"description":"(SmartPhoneUtil-A-2013) Action is forbidden. secretKnowledge is missing but required!"}}```

An addition field must be included
* `serviceType=DOOR_UNLOCK`
* `bmwSkAnswer=BMW_ACCOUNT_SECURITY_QUESTION_ANSWER`


#### Flash the headlights
If you can't find the vehicle, or need to illuminate something in its vicinity, you can briefly activate the headlights.

* `serviceType=LIGHT_FLASH&count=2`
    * I assume that `count` relates to the number of seconds to keep the light on?

#### Charging Schedule
Set the peak / off peak charging schedule.

* `serviceType=CHARGING_CONTROL`
    * Additional data needs to be sent as parameter `data` in JSON format. The data itself is the same as returned by [Get Charging Times](#get-charging-times).
    * Instead of `weeklyPlanner` `twoTimesTimer` can be used. Format of data currently unknown.
```
# Notes:
# - Linebreaks for "data" have been added for readability only.
curl -i \
  -X POST \
  -H "Content-Type: application/x-www-form-urlencode" \
  --data-urlencode 'serviceType=CHARGING_CONTROL' \
  --data-urlencode 'data={
    "weeklyPlanner":
      {
        "climatizationEnabled": true,
        "chargingMode": "IMMEDIATE_CHARGING",
        "chargingPreferences": "CHARGING_WINDOW",
        "timer1":{
          "departureTime": "12:30",
          "timerEnabled": true,
          "weekdays": []
        },
        "timer2":{
          "weekdays": []
        },
        "timer3":{
          "departureTime": "19:30",
          "timerEnabled": false,
          "weekdays": []
        },
        "overrideTimer": {
          "weekdays": []
        },
        "preferredChargingWindow": {
          "enabled": false,
          "startTime": "00:00",
          "endTime": "00:00"
        }}}' \
  https://b2vapi.bmwgroup.com/webapi/v1/user/vehicles/:VIN/executeService
```

#### Vehicle Finder
* `serviceType=VEHICLE_FINDER`
    * I'm not sure what this does.

#### Response

An example response for all `POST` commands:
```
{
    "executionStatus": {
        "serviceType": "LIGHT_FLASH",
        "status": "INITIATED",
        "eventId": "123456789012345AB1CD1234@bmw.de"
    }
}
```

### Send POI

Sending a POI to the car.

* `POST /webapi/v1/user/vehicles/:VIN/sendpoi`
    * Where `:VIN` is your vehicle's VIN.
    * Remember to include the `Authorization: Bearer` header.
    * Remember to include the `Content-Type: application/x-www-form-urlencode` header.

#### Body
```
body={
	"poi": {
		"city": "abc",
		"lat": nn.nnn,
		"lon": nn.nnn,
		"name": "name",
		"rating": -1,
		"postalCode": "12345",
		"street": "Musterstr. 6"
	}
}
```
#### Response
HTTP 204

## What's Next?

Using these commands you should be able to replicate the functionality of the official app.

If you spot any errors or omissions, please raise an issue or send a Pull Request.
