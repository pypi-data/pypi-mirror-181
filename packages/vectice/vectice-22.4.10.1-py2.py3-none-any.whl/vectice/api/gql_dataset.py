from typing import Union, List, Optional
import logging
from gql import gql
from gql.transport.exceptions import TransportQueryError

from vectice.api.gql_api import GqlApi, Parser
from vectice.api.json.metadata import MetadataInput, MetadataOutput
from vectice.api.json.dataset_register import DatasetRegisterInput, DatasetRegisterOutput
from vectice.models.dataset_type import DatasetType


_logger = logging.getLogger(__name__)

# TODO JobRun for lineages
_RETURNS = """
            datasetVersion{
                          id
                          name
            }
            useExistingDataset
            useExistingVersion
            __typename
            """


class GqlDatasetApi(GqlApi):
    def create_dataset(
        self,
        project_id: int,
        dataset_name: str,
        dataset_type: DatasetType,
        metadata: Union[MetadataInput, List[MetadataInput]],
        phase_id: Optional[int],
        iteration_id: Optional[int],
        inputs: Optional[List[str]],
    ):
        query = gql(
            f"""
                    query createMetadata {{
                        createMetadata(
                            projectId: {project_id}
                            datasetName: {dataset_name}
                            datasetType: {dataset_type}
                            metadata: {metadata}
                            phaseId: {phase_id}
                            iterationId: {iteration_id}
                            inputs: {inputs}
                        ) {{
                            dataset
                            datasetVersion
                            isNewCsvCreated
                        }}
                    }}
                """
        )
        try:
            response = self.execute(query)
            result = MetadataOutput(response["createMetadata"])
            return result
        except TransportQueryError as e:
            raise self._error_handler.handle_post_gql_error(e, "dataset", dataset_name)

    def register_dataset(
        self,
        data: DatasetRegisterInput,
        project_id: Optional[int] = None,
        phase_id: Optional[int] = None,
        iteration_id: Optional[int] = None,
    ) -> DatasetRegisterOutput:
        if phase_id and project_id:
            variable_types = "$projectId:Float!,$phaseId:Float!,$data:DatasetRegisterInput!"
            kw = "projectId:$projectId,phaseId:$phaseId,data:$data"
            variables = {"projectId": project_id, "phaseId": phase_id, "data": data}
        elif iteration_id and project_id:
            variable_types = "$projectId:Float!,$iterationId:Float!,$data:DatasetRegisterInput!"
            kw = "projectId:$projectId,iterationId:$iterationId,data:$data"
            variables = {"projectId": project_id, "iterationId": iteration_id, "data": data}
        elif project_id:
            variable_types = "$projectId:Float!,$data:DatasetRegisterInput!"
            kw = "projectId:$projectId,data:$data"
            variables = {"projectId": project_id, "data": data}
        else:
            raise RuntimeError("The provided parent child ids do not match!")

        query = GqlApi.build_query(
            gql_query="registerDataset",
            variable_types=variable_types,
            returns=_RETURNS,
            keyword_arguments=kw,
            query=False,
        )
        query_built = gql(query)
        try:
            response = self.execute(query_built, variables)
            dataset_output: DatasetRegisterOutput = Parser().parse_item(response["registerDataset"])
            return dataset_output
        except TransportQueryError as e:
            raise self._error_handler.handle_post_gql_error(e, "dataset", "register dataset")
