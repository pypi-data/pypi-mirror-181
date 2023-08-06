from __future__ import annotations

import urllib
from typing import Optional, Union

from .rest_api import RestApi, HttpError
from .json import DatasetOutput
from .project import ProjectApi
from .http_error_handlers import InvalidReferenceError, MissingReferenceError


class DatasetApi(RestApi):
    def get_dataset(
        self,
        dataset: Union[str, int],
        project: Optional[Union[str, int]] = None,
        workspace: Optional[Union[str, int]] = None,
    ) -> DatasetOutput:
        if not isinstance(dataset, int) and not isinstance(dataset, str):
            raise InvalidReferenceError("dataset", dataset)
        if isinstance(dataset, int):
            parent_project = None
            url = f"/metadata/dataset/{dataset}"
        else:
            if project is None:
                raise MissingReferenceError("dataset", "project")
            parent_project = ProjectApi(self.auth).get_project(project, workspace)
            url = f"/metadata/project/{parent_project.id}/dataset/name/{urllib.parse.quote(dataset)}"
        try:
            response = self.get(url)
            result = DatasetOutput(**response)
            if parent_project is not None:
                result.project = parent_project
            return result
        except HttpError as e:
            raise self._httpErrorHandler.handle_get_http_error(e, "dataset", dataset)
        except IndexError:
            raise ValueError("The dataset is invalid. Please check the entered value.")
