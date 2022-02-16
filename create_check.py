import requests
import json
import logging

logging.basicConfig(filename="log.txt", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")


class CreateCheck:
    def __init__(self, api_url2, api_key2, check_type, req_body):
        self.api_url2 = api_url2
        self.api_key2 = api_key2
        l_string = "/v3/Checks/"
        # need function
        self.check_type = check_type
        headers = {'Content-Type': 'application/json'}
        self.req_body = req_body
        self.url = api_url2 + l_string + check_type
        logging.info(f'Creating new check')
        self.response = requests.post(self.url, params=self.api_key2, data=json.dumps(self.req_body), timeout=2,
                                      headers=headers)
        self.status_code = self.response
        logging.debug(self.status_code)
        logging.info(self.response.headers)
        location_address = str(self.response.headers["Location"])
        api_string = str.lower(api_url2+l_string)
        self.new_check_id = location_address.replace(api_string, "")

