import json
from json import JSONDecodeError


class Configuration:
    def __init__(self, config_file_path: str):
        with open(config_file_path, "r") as config_file:
            try:
                config_object = json.load(config_file)
                self._workspace = config_object.get("WORKSPACE")
                self._project = config_object.get("PROJECT")
                self._api_token = config_object["VECTICE_API_TOKEN"]
                self._host = config_object["VECTICE_API_ENDPOINT"]
            except JSONDecodeError:
                raise SyntaxError("The json config file could not be read. Check that the file structure is valid.")
            except KeyError as error:
                raise KeyError(f"The key {error.args[0]} is required in the json config file.")

    @property
    def workspace(self):
        return self._workspace

    @property
    def project(self):
        return self._project

    @property
    def api_token(self):
        return self._api_token

    @property
    def host(self):
        return self._host
