from mitmproxy import http
import logging
import json


class HTTPLoggerTools:

    request_payload = []
    response_payload = []
    session_request_path = ""

    def __init__(self):
        logging.info("Starting logger tool")
        self.num = 0

    def request(self, flow: http.HTTPFlow):
        self.session_request_path = flow.request.path
        if ("/api/v1/" in self.session_request_path):
            if (flow.request.method != "GET"):
                logging.info("Found request pattern from configured URL: %s",
                             flow.request.url)
                self.request_payload.append(json.loads(flow.request.content))

    def response(self, flow: http.HTTPFlow):
        if ("/api/v1/" in self.session_request_path):
            logging.info("Found response data from configured URL: %s",
                         flow.request.url)
            self.response_payload.append(json.loads(flow.response.content))

    def client_disconnected(self, data):
        if ("/api/v1" in self.session_request_path):
            self.request_payload.extend(self.response_payload)
            logging.info("Merged - %s", self.request_payload)

            self.num = self.num + 1
            path = "c:\\temp\\filename_" + str(self.num) + ".json"
            with open(path, "w") as write_file:
                json.dump(self.request_payload, write_file, indent=4)

            self.request_payload = []
            self.response_payload = []


addons = [HTTPLoggerTools()]
