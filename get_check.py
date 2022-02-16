import requests
import logging

logging.basicConfig(filename="log.txt", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")


class GetChecks:
    def __init__(self, api_url1, api_key1, check_id):
        self.api_url1 = api_url1
        self.api_key1 = api_key1
        self.check_id = check_id
        self.l_string = "/v3/Checks/"
        self.url = str(self.api_url1 + self.l_string + self.check_id)
        logging.info(f'Creating request for checkID {self.check_id}')
        self.response = requests.get(self.url, params=api_key1, timeout=3).json()
        logging.info(f'Getting check details {self.response}')
        self.check_url = self.response["url"]
        self.check_name = self.response["name"]
        self.check_type = self.response["check_type_api"]
        self.location = self.response["location"].split(',')[1].lstrip()
        self.enabled = self.response["enabled"]
        self.interval_seconds = self.response["interval_seconds"]
        self.tags = self.response["tags"]
        self.scheduled_inclusion = self.response["scheduled_inclusion"]
        self.scheduled_exclusion = self.response["scheduled_exclusion"]
