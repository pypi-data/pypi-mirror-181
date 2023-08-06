from __future__ import annotations

import urllib
from typing import Optional, Union

from .dataset import DatasetApi
from .http_error_handlers import MissingReferenceError
from .json import DatasetVersionOutput
from .rest_api import RestApi, HttpError


class DatasetVersionApi(RestApi):
    def get_dataset_version(
        self,
        version: Union[str, int],
        dataset: Optional[Union[str, int]] = None,
        project: Optional[Union[str, int]] = None,
        workspace: Optional[Union[str, int]] = None,
    ) -> DatasetVersionOutput:
        if not isinstance(version, int) and not isinstance(version, str):
            raise ValueError("The dataset version reference is invalid. Please check the entered value.")
        if isinstance(version, int):
            url = f"/metadata/datasetversion/{version}"
        else:
            if dataset is None:
                raise MissingReferenceError("dataset version", "dataset")
            parent_dataset = DatasetApi(self.auth).get_dataset(dataset, project, workspace)
            url = f"/metadata/project/{parent_dataset.project.id}/dataset/{parent_dataset.id}/version/name/{urllib.parse.quote(version)}"
        try:
            response = self.get(url)
            return DatasetVersionOutput(**response)
        except HttpError as e:
            raise self._httpErrorHandler.handle_get_http_error(e, "dataset version", version)
        except IndexError:
            raise ValueError("The dataset version is invalid. Please check the entered value.")
