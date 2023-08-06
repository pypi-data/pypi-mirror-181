from __future__ import annotations

from typing import List, Dict, Any, Type, TypeVar, Union
from gql import Client

from vectice.api._auth import Auth
from vectice.api.http_error_handlers import ClientErrorHandler
from vectice.api.json import UserActivity
from vectice.api.json import (
    WorkspaceOutput,
    PagedResponse,
    ProjectOutput,
    PhaseOutput,
    StepOutput,
    IterationOutput,
    DatasetRegisterOutput,
    ModelRegisterOutput,
    CodeOutput,
    CodeVersionOutput,
)

ResultType = TypeVar("ResultType")


# TODO DatasetRegisterResultOutput
class Parser:
    def map_type(self, type_name: str) -> Type[ResultType]:
        types_map = {
            "Workspace": WorkspaceOutput,
            "Project": ProjectOutput,
            "Phase": PhaseOutput,
            "IterationStep": StepOutput,
            "Iteration": IterationOutput,
            "DatasetRegisterResultOutput": DatasetRegisterOutput,
            "ModelRegisterResultOutput": ModelRegisterOutput,
            "UserActivity": UserActivity,
            "Code": CodeOutput,
            "CodeVersion": CodeVersionOutput,
        }
        if type_name in types_map.keys():
            return types_map[type_name]  # type: ignore
        else:
            raise RuntimeError("Unknown type: " + type_name)

    def parse_item(self, item: Dict[str, Any]) -> ResultType:  # type: ignore
        clazz: Type[ResultType] = self.map_type(item["__typename"])
        result = clazz(**item)
        return result

    def parse_list(self, list: List[Dict[str, Any]]) -> List[ResultType]:
        result: List[ResultType] = []
        for item in list:
            result.append(self.parse_item(item))
        return result

    def parse_paged_response(self, data: Dict[str, Any]) -> PagedResponse[ResultType]:
        return PagedResponse(data["total"], data["page"], self.map_type(data["items"][0]["__typename"]), data["items"])

    def parse(self, data) -> Union[ResultType, List[ResultType], PagedResponse[ResultType]]:
        if type(data) == list:
            return self.parse_list(data)
        else:
            if "items" in data and "page" in data and "total" in data:
                return self.parse_paged_response(data)
            else:
                return self.parse_item(data)


class GqlApi:
    def __init__(self, client: Client, auth: Auth):
        self.client = client
        self.auth = auth
        self._error_handler = ClientErrorHandler()

    def execute(self, query, variables=None):
        # retrieve auth & sdk http headers
        self.client.transport.headers = self.auth.http_headers
        return self.client.execute(query, variables)

    @staticmethod
    def build_query(gql_query, variable_types, returns, keyword_arguments, query=True):
        if query:
            query_type = "query"
        else:
            query_type = "mutation"
        query_built = """
        %(query_type)s %(gql_query)s(%(variable_types)s) {
            %(gql_query)s(%(keyword_arguments)s) {
                %(returns)s
            }
        }
        """ % {
            "query_type": query_type,
            "gql_query": gql_query,
            "variable_types": variable_types,
            "keyword_arguments": keyword_arguments,
            "returns": returns,
        }
        return query_built
