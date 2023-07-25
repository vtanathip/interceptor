import os
import json
from mitmproxy import http
import re
import logging

CONFIG_FOLDER = "config"
DATA_FOLDER = "data"
SCRIPT_PATH = os.path.abspath(__file__)
ROOT_DIRECTORY = os.path.dirname(os.path.dirname(SCRIPT_PATH))


class JsonLoader:
    def __init__(self, file_name):
        self.file_name = file_name

    def load_data(self):
        try:
            file_path = os.path.abspath(self.file_name)
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file '{self.file_name}' not found.")
        except json.JSONDecodeError:
            raise ValueError(
                f"Error decoding JSON in file '{self.file_name}'.")


class MockingBird:

    def __init__(self):
        mockfile = os.path.join(ROOT_DIRECTORY,
                                f'{CONFIG_FOLDER}\mock.json')
        loader = JsonLoader(mockfile)
        logging.info("Starting Mocking tool")
        self.config_data = {}
        self.response_flag = False
        try:
            self.config_data = loader.load_data()
        except Exception as e:
            print("Error while load config:", e)

    def all_keywords_in_url(self, keywords, url):
        for keyword in keywords:
            pattern = r"\b%s\b" % re.escape(keyword)
            if not re.search(pattern, url):
                return False
        return True

    def request(self, flow: http.HTTPFlow):
        for config in self.config_data["mock_services"]:
            print("patterns ", config["request_patterns"])
            full_url = f"{flow.request.host}{flow.request.path}"
            if self.all_keywords_in_url(config["request_patterns"], full_url):
                self.response_flag = True
                self.data_file = config["data_file"]
            else:
                self.response_flag = False
                self.data_file = None

    def response(self, flow: http.HTTPFlow):
        print("finished response")
        if self.response_flag:
            datafile = os.path.join(ROOT_DIRECTORY,
                                    f'{DATA_FOLDER}\{self.data_file}')
            response_data = JsonLoader(datafile)
            json_response = json.dumps(response_data.load_data())
            flow.response = http.Response.make(
                200,              # Status code
                json_response,    # Response content (JSON data as a string)
                {"Content-Type": "application/json"}  # Headers
            )


addons = [MockingBird()]


''' For test local run before using mitm '''
# a = MockingBird()
# a.request()
