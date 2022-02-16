import csv
import logging

from create_check import CreateCheck
from get_check import GetChecks
from get_items import GetLocation, GetGroups

logging.basicConfig(filename="log.txt", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")

api_url1 = input("Endpoint1 url (i.e. 'http(s)://api-wpm.apicasystem.com'): ")
authkey1 = input("Endpoint1 auth_ticket:")
api_url2 = input("Endpoint2 url (i.e. 'http(s)://api-wpm2.apicasystem.com'): ")
authkey2 = input("Endpoint2 auth_ticket:")

api_key1 = {"auth_ticket": authkey1}
api_key2 = {"auth_ticket": authkey2}

# Global Variables to string match with API and Py
false = "false"
true = "true"

print("starting check migration...")
with open('checks.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    # next(csv_reader)
    line_count = 0
    for row in csv_reader:
        check_id = row['check_id']
        check_type = row['check_type']
        check_name = row['check_name']
        check_location = row['check_location']
        print(f'old check info: {check_id}, {check_type}, {check_name}, {check_location}')
        logging.info("----------------CREATING NEW CHECK----------------")
        get_Check = GetChecks(api_url1, api_key1, check_id)
        get_Location = GetLocation(api_url2, api_key2, check_type, get_Check.location)

        get_Groups = GetGroups(api_url2, api_key2)

        req_body = {
            "url": get_Check.check_url,
            "name": get_Check.check_name,
            "description": "",
            "monitor_groups_ids": [get_Groups.subgroup["id"]],  # if using monitor groups, uncomment and use get_Groups object
            "interval_seconds": get_Check.interval_seconds,
            "location_code": get_Location.all_locations["location_code"],
            "check_fail_severity": "F",
            "scheduled_inclusion": get_Check.scheduled_inclusion,
            "scheduled_exclusion": get_Check.scheduled_exclusion,
            "tags": get_Check.tags
        }
        logging.info(req_body)

        create_Check = CreateCheck(api_url2, api_key2, get_Check.check_type, req_body)

        # GETTING NEW CHECK DATA - Validation
        if str(create_Check.status_code) == "<Response [201]>":
            get_New_Check = GetChecks(api_url2, api_key2, create_Check.new_check_id)
            logging.info(
                get_New_Check.check_id + ", " + get_New_Check.check_type + ", " + get_New_Check.check_name + ", " + get_New_Check.check_url + ", " + get_New_Check.location)
            logging.info("status: success")
            print(
                f'new check info: {get_New_Check.check_id}, {get_New_Check.check_type}, {get_New_Check.check_name}, {get_New_Check.check_url}, {get_New_Check.location}')
        else:
            logging.error(f"check " + {check_id} + " could not be recreated")
            print("status: error")
            print(f"check " + {check_id} + " could not be recreated")
        with open('checks_output.csv', 'a', newline='') as csv_file2:
            fieldnames = ["old_check_id", "old_check_type", "old_check_name", "old_check_location", "new_check_id",
                          "new_check_type", "new_check_name", "new_check_url", "new_check_location"]
            csv_writer = csv.DictWriter(csv_file2, fieldnames=fieldnames, delimiter=',')
            csv_writer.writerow({"old_check_id": check_id,
                                 "old_check_type": check_type,
                                 "old_check_name": check_name,
                                 "old_check_location": check_location,
                                 "new_check_id": get_New_Check.check_id,
                                 "new_check_type": get_New_Check.check_type,
                                 "new_check_name": get_New_Check.check_name,
                                 "new_check_url": get_New_Check.check_url,
                                 "new_check_location": get_New_Check.location
                                 })
        csv_file2.close()
csv_file.close()
print("MIGRATION COMPLETE (please review checks_output.csv)")
