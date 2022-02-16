# url-check-migration-python

A python script using Apica API's to migrate URL checks between environments

#### Requirements:
* Python 3.9
* Install requests library

#### Quick Start
1. Load "checks.csv" with check info that will be migrated, using the following format: check_id,check_type,check_name,check_location
Tip: list 50 max checks at time so the API server dosnt get overloaded with requests

2. Input Parameters- you will be prompted for API information:
Endpoint1 url (i.e. 'http(s)://api-wpm.apicasystem.com'):
Endpoint1 auth_ticket:
Endpoint2 url (i.e. 'http(s)://api-wpm2.apicasystem.com'):
Endpoint2 auth_ticket:

3. Begin Test
An iteration of old check info and new check info will start displaying until complete.
You can also review log.txt and checks_output.csv for more info. 

#### checks_output.csv - displays old check info and new check info in csv format
