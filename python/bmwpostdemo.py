#! /usr/bin/env python
#
# Here's a simple script to flash the headlights, as 
# a demo of requesting a service.
#
# Quentin Stafford-Fraser 2016

import bmw
import time

c = bmw.ConnectedDrive()
resp = c.call('/user/vehicles/')
vin = resp['vehicles'][0]['vin']

service = 'LIGHT_FLASH'  # or DOOR_LOCK, DOOR_UNLOCK etc
print "Sending {} request...".format(service)
resp = c.executeService(vin, service)
status = resp['executionStatus']['status']
while status in ('INITIATED','PENDING'):
    print status
    time.sleep(2)
    check = c.call('/user/vehicles/{}/serviceExecutionStatus?serviceType={}'.format(vin, service))
    status = check['executionStatus']['status']

print status
