import requests
import logging

logging.basicConfig(filename="log.txt", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")


class GetLocation:
    def __init__(self, api_url2, api_key2, check_type, old_location):
        self.api_url = api_url2
        self.api_key = api_key2
        self.check_type = check_type
        self.old_location = old_location
        if self.check_type == "url":
            check_type = "url"
        elif self.check_type == "ping":
            check_type = "ping"
        else:
            check_type = "port"
        l_string = "/v3/checks/" + check_type + "/locations?"
        logging.info("Grabbing Geolocation IDs")
        self.response = requests.get(api_url2 + l_string, params=api_key2, timeout=3).json()
        logging.info(self.response)
        for i in range(len(self.response)):
            if check_type != "url-v2":
                region = (self.response[i]["region"])
                if self.old_location == region:
                    self.all_locations = {
                        "region": (self.response[i]["region"]),
                        "country": (self.response[i]["country"]),
                        "location_code": (self.response[i]["location_code"])
                    }
            else:
                region = (self.response[i]["city"])
                if self.old_location == region:
                    self.all_locations = {
                        "region": (self.response[i]["city"]),
                        "country": (self.response[i]["country"]),
                        "location_code": (self.response[i]["location_code"])
                    }

        logging.info(self.all_locations["location_code"])


class GetGroups:
    def __init__(self, api_url2, api_key2):
        self.api_url = api_url2
        self.api_key = api_key2
        l_string = "/v3/groups"
        logging.info("Grabbing Group IDs")
        monitoring_groups = []
        self.response = requests.get(api_url2 + l_string, params=api_key2, timeout=3).json()
        for i in range(len(self.response)):
            self.groups = (self.response[i]["groups"])
            for x in range(len(self.groups)):
                group_id = (self.groups[x]["id"])
                group_name = (self.groups[x]["name"])
                self.subgroup = {
                    "id": group_id,
                    "name": group_name
                }
                monitoring_groups.append(self.subgroup)
        logging.info(monitoring_groups)
