#! /usr/bin/env python
#
# Here's a simple script to flash the headlights, as 
# a demo of requesting a service.
#
# Quentin Stafford-Fraser 2016

import bmw
import time

c = bmw.ConnectedDrive()
resp = c.call('/user/vehicles')
vin = resp['vehicles'][0]['vin']

service = 'DOOR_UNLOCK'  # or DOOR_LOCK, DOOR_UNLOCK etc
secret = 'My Super Secret Unlock Passcode'
resp = c.executeService2(vin, service, secret)
status = resp['executionStatus']['status']
while status in ('INITIATED','PENDING'):
    print status
    time.sleep(2)
    check = c.call('/user/vehicles/{}/serviceExecutionStatus?serviceType={}'.format(vin, service))
    status = check['executionStatus']['status']
print status
