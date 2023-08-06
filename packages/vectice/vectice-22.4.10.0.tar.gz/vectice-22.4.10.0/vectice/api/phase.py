from __future__ import annotations

import logging
from typing import List, Optional, Union

from gql import gql
from gql.transport.exceptions import TransportQueryError

from vectice.api.gql_api import GqlApi, Parser
from vectice.api.json.phase import PhaseOutput


_RETURNS = """id
              name
              alias
              status
              index
              __typename
            """


_logger = logging.getLogger(__name__)


class PhaseApi(GqlApi):
    def list_phases(self, parent_id: int, search_alias: Optional[str] = None) -> List[PhaseOutput]:
        alias_filter = {
            "parentId": parent_id,
            "searchFilter": {"search": search_alias if search_alias is not None else "", "fields": "name"},
        }

        variable_types = "$filters:PhaseFiltersInput!"
        kw = "filters:$filters"
        variables = {"filters": alias_filter}
        returns = f"""items{{
                    {_RETURNS}
        }}"""
        query = GqlApi.build_query(
            gql_query="getPhaseList", variable_types=variable_types, returns=returns, keyword_arguments=kw, query=True
        )
        query_built = gql(query)
        try:
            response = self.execute(query_built, variables)
            phase_output: List[PhaseOutput] = Parser().parse(response["getPhaseList"]["items"])  # type: ignore
            return phase_output
        except TransportQueryError as e:
            raise self._error_handler.handle_post_gql_error(e, "phase", "list")

    def get_phase(self, phase: Union[str, int], parent_id: Optional[int] = None) -> PhaseOutput:
        """
        parent_id is the project id
        """
        if isinstance(phase, int):
            gql_query = "getPhaseById"
            variable_types = "$id:Float!"
            variables = {"id": phase}
            kw = "id:$id"
        elif isinstance(phase, str) and parent_id:
            gql_query = "getPhaseByName"
            variable_types = "$name:String!,$parentId:Float!"
            variables = {"name": phase, "parentId": parent_id}  # type: ignore
            kw = "name:$name,parentId:$parentId"
        else:
            raise ValueError("string and parent id required.")
        query = GqlApi.build_query(
            gql_query=gql_query, variable_types=variable_types, returns=_RETURNS, keyword_arguments=kw, query=True
        )
        query_built = gql(query)
        try:
            response = self.execute(query_built, variables)
            phase_output: PhaseOutput = Parser().parse_item(response[gql_query])
            return phase_output
        except TransportQueryError as e:
            raise self._error_handler.handle_post_gql_error(e, "phase", phase)
