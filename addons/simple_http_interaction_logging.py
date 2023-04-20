"""
Basic skeleton of a mitmproxy addon.

Run as follows: mitmproxy -s anatomy.py
"""
from mitmproxy import http
import logging
import json


class UrlLogging:
    def __init__(self):
        logging.info("Track Request")

    def request(self, flow: http.HTTPFlow):
        self.method = flow.request.method
        self.host = flow.request.host
        self.port = flow.request.port
        self.path = flow.request.path
        self.headers = flow.request.headers
        self.content = flow.request.content
        logging.info("URL Path: %s",
                     self.host + self.path)
        logging.info("URL Path: %s",
                     json.loads(self.content))

    def response(self, flow: http.HTTPFlow):
        logging.info("Response data: %s",
                     json.loads(flow.response.content))


addons = [UrlLogging()]
