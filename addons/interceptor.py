import os
import json
from mitmproxy import http
import re


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
    def all_keywords_in_url(self, keywords, url):
        for keyword in keywords:
            pattern = r"\b%s\b" % re.escape(keyword)
            if not re.search(pattern, url):
                return False
        return True

    def response(self, flow: http.HTTPFlow):
        print("Mock response")

    def test(self):
        loader = JsonLoader("config/mock.json")
        try:
            data = loader.load_data()
            print("Name:", data["mock_services"][0])
        except Exception as e:
            print("Error:", e)


addons = [MockingBird()]

''' For test local run before using mitm '''
# a = MockingBird()
# a.test()
