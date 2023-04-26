from mitmproxy import http
import logging
import json
from configparser import ConfigParser
import os


class HTTPLoggerTools:

    request_payload = []
    response_payload = []
    session_request_path = ""
    url_path_for_log = ""
    log_location = ""

    def __init__(self):
        logging.info("Starting logger tool")
        self.num = 0
        self.read_configuration_file()

    def request(self, flow: http.HTTPFlow):
        self.session_request_path = flow.request.path
        if (self.url_path_for_log in self.session_request_path):
            if (flow.request.method != "GET"):
                logging.info("Request pattern from configured URL: %s",
                             flow.request.url)
                headersdata = {
                    "headers": {
                        "User-Agent": flow.request.headers['User-Agent']
                    }
                }
                self.request_payload.append(
                    headersdata)
                request_body = {
                    "request_body": json.loads(flow.request.content)
                }
                self.request_payload.append(request_body)

    def response(self, flow: http.HTTPFlow):
        if (self.url_path_for_log in self.session_request_path):
            logging.info("Response data from configured URL: %s",
                         flow.request.url)
            http_response_data = {
                "http_response_code": flow.response.status_code
            }
            self.response_payload.append(http_response_data)
            self.request_payload.extend(self.response_payload)
            logging.info("Merged - %s", self.request_payload)
            self.logging_to_file()
            self.request_payload = []
            self.response_payload = []

    def logging_to_file(self):
        path = self.gen_filename()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as write_file:
            json.dump(self.request_payload, write_file, indent=4)

    def gen_filename(self):
        self.num = self.num + 1
        return self.log_location + "\http_log_" + str(self.num) + ".json"

    def read_configuration_file(self):
        thisfolder = os.path.dirname(os.path.abspath(__file__))
        initfile = os.path.join(thisfolder, 'logger.cfg')
        logging.info(thisfolder)
        parser = ConfigParser()
        parser.read(initfile)
        self.url_path_for_log = parser.get('logger', 'url')
        self.log_location = parser.get('logger', 'loglocation')


addons = [HTTPLoggerTools()]
