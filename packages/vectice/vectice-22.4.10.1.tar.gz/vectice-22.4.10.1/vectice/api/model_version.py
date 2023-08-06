from __future__ import annotations

import logging
import urllib
from typing import Optional, Union

from .rest_api import RestApi, HttpError
from ._auth import Auth
from .json import ModelVersionOutput
from .model import ModelApi
from .http_error_handlers import MissingReferenceError


_logger = logging.getLogger(__name__)


class ModelVersionApi(RestApi):
    def __init__(self, auth: Auth):
        super().__init__(auth)

    def get_model_version(
        self,
        version: Union[str, int],
        model: Optional[Union[str, int]],
        project: Optional[Union[str, int]] = None,
        workspace: Optional[Union[str, int]] = None,
    ) -> ModelVersionOutput:
        if not isinstance(version, int) and not isinstance(version, str):
            raise ValueError("The model version reference is invalid. Please check the entered value.")

        if isinstance(version, int):
            url = f"/metadata/modelversion/{version}"
        elif isinstance(version, str):
            if model is None:
                raise MissingReferenceError("model version", "model")
            parent_model = ModelApi(self.auth).get_model(model, project, workspace)
            url = f"/metadata/project/{parent_model.project.id}/model/{parent_model.id}/version/name/{urllib.parse.quote(version)}"
        try:
            response = self.get(url)
            return ModelVersionOutput(**response)
        except HttpError as e:
            raise self._httpErrorHandler.handle_get_http_error(e, "model version", version)
        except IndexError:
            raise ValueError("The model version is invalid. Please check the entered value.")
