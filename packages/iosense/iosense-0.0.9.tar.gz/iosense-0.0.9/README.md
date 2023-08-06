[![](https://mail.google.com/mail/u/1?ui=2&ik=a639aca6e2&attid=0.0.3&permmsgid=msg-a:r6478207869088414184&th=184f04903eb9cef5&view=fimg&fur=ip&sz=s0-l75-ft&attbid=ANGjdJ83kO7qn2b0dmHCuDa9iVD7U9jk6478Bxov76KIx2l_llkVI63YVcsVog9Uctah56WURAl49iw5DjonpFeZaV8WYabp9uEajY340GTZ7Fbr3z78E-ihNGGTsyg&disp=emb&realattid=ii_k61z5hii2)](https://faclon.com)
# Faclon I/O Sense Data Access API

​
## Where to get it


 PyPI

`pip install iosense`


`pip3 install iosense`

​
# Features
## Access time based Device Sensor Data
Function to retrive sensor data of a single device in the defined time range.
​
This is a cursor based paginated request and it consumes 1 API request for one time request that contain a maximum of 10000 data points only and a cursor pointing to the next start and end time. So the API count will have to be called recursively until either the cursor.start or cursor.end is null.
​
start time - unix timestamp
end time - unix timestamp
deviceID - string
sensorID - string (comma seperated list of sensorIDs)
Note- In the response, data is in descending order by time
​
​

## GET All Sensor Data
Function to retrive data of single device and all sensors of that device in a given time range.
​
This is a cursor based paginated request i.e. at one time the response will contain a maximum of 10000 data points only and a cursor pointing to the next start and end time. So this API will have to be called recursively until either the cursor.start or cursor.end is null.
​
start time - unix timestamp
end time - unix timestamp
deviceID - string
Note- In the response, data is in descending order by time
​
## GET Last Data Point
Function to retrive the value of the most recent data of a single device single sensor
​
deviceID - string
sensorID - string
​

## Get Last n Data Points Before Time Multiple Sensor
Function to retrive last n data points of a single device single sensor with a given end time.
​
This is a cursor based paginated request i.e. at one time the response will contain a maximum of 10000 data points only and a cursor pointing to the end time and a new limit. So this API will have to be called recursively until either the cursor.end is null or limit is null.
​
end time - unix timestamp
deviceID - string
sensor - string (comma seperated list of sensorIDs)
lim - integer
Note- In the response, data is in descending order by time
​
Note- If limit>10000, in each response you will get new limit. So if limit is 25000, in the response the new limit is 15000 which will have to be used in the new request.
​
​
## Get Device ID, DeviceType ID
Endpoint to retrive deviceID and deviceTypeID of all devices added in user account
​
## Get Device metaData
Endpoint to get all metadata of a single device
​
​
## Dependencies
`pandas, requests, json, time, datetime, sys
`​
​
​
## License
MIT
​
## Documentation
The official documentation is hosted on 
​
## Reach us
For usage questions, please reach out to us at reachus@faclon.com
