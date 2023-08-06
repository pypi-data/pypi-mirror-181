from vectice.api.rest_api import RestApi
from vectice.api.json.compatibility import CompatibilityOutput


class CompatibilityApi(RestApi):
    def check_version(self) -> CompatibilityOutput:
        response = self.get("/metadata/compatibility")
        if "message" not in response.keys():
            return CompatibilityOutput(message="", status="OK")
        else:
            return CompatibilityOutput(**response)
