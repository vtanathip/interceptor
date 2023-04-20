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
                logging.info("Found request pattern from configured URL: %s",
                             flow.request.url)
                self.request_payload.append(json.loads(flow.request.content))

    def response(self, flow: http.HTTPFlow):
        if (self.url_path_for_log in self.session_request_path):
            logging.info("Found response data from configured URL: %s",
                         flow.request.url)
            self.response_payload.append(json.loads(flow.response.content))

    def client_disconnected(self, data):
        if (self.url_path_for_log in self.session_request_path):
            self.request_payload.extend(self.response_payload)
            logging.info("Merged - %s", self.request_payload)

            self.num = self.num + 1
            path = self.log_location + "\http_log_" + str(self.num) + ".json"
            with open(path, "w") as write_file:
                json.dump(self.request_payload, write_file, indent=4)

            self.request_payload = []
            self.response_payload = []

    def read_configuration_file(self):
        thisfolder = os.path.dirname(os.path.abspath(__file__))
        initfile = os.path.join(thisfolder, 'logger.cfg')
        logging.info(thisfolder)
        parser = ConfigParser()
        parser.read(initfile)
        self.url_path_for_log = parser.get('logger', 'url')
        self.log_location = parser.get('logger', 'loglocation')


addons = [HTTPLoggerTools()]
