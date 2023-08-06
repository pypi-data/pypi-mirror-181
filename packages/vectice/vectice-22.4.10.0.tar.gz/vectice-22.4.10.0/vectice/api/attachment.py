from __future__ import annotations

import logging
from io import BytesIO
from typing import Optional, Tuple, Any, BinaryIO, Union, Sequence, cast, NoReturn, List

from vectice.api._auth import Auth
from vectice.api.dataset_version import DatasetVersionApi
from vectice.api.model_version import ModelVersionApi
from vectice.api.project import ProjectApi
from .rest_api import RestApi, HttpError
from .json import PagedResponse, AttachmentOutput, DatasetVersionOutput, ModelVersionOutput
from .http_error_handlers import InvalidReferenceError, MissingReferenceError


NO_ARTIFACT_REFERENCE_PROVIDED = "No reference to artifact or artifact version provided."
PROJECT = "project"


class AttachmentApi(RestApi):
    def __init__(self, auth: Auth):
        super().__init__(auth)
        self._logger = logging.getLogger(self.__class__.__name__)

    def _generate_artifact_url_and_id(
        self,
        _type: str,
        version: Optional[Union[str, int]] = None,
        artifact: Optional[Union[str, int]] = None,
        workspace: Optional[Union[str, int]] = None,
        project: Optional[Union[str, int]] = None,
    ) -> Tuple[str, Optional[str]]:
        url = None
        object_name = None
        try:
            if _type == "datasetversion":
                version = self._get_version_reference(_type, version, project)
                url, object_name = self.get_url_and_id_for_dataset_version(_type, version, artifact, workspace, project)
            elif _type == "modelversion":
                version = self._get_version_reference(_type, version, project)
                url, object_name = self.get_url_and_id_for_model_version(_type, version, artifact, workspace, project)
            elif _type == PROJECT:
                url = self.get_url_for_project(_type, workspace, project)
            if url is None:
                raise RuntimeError("url cannot be none")
            return url, object_name
        except HttpError as e:
            self._handle_http_error(e, _type, version, artifact)

    def get_url_and_id_for_dataset_version(
        self,
        _type: str,
        version: Union[str, int],
        artifact: Optional[Union[str, int]] = None,
        workspace: Optional[Union[str, int]] = None,
        project: Optional[Union[str, int]] = None,
    ) -> Tuple[str, str]:
        version_object: DatasetVersionOutput = DatasetVersionApi(self.auth).get_dataset_version(
            version=version, dataset=artifact, project=project, workspace=workspace
        )
        url = self._build_url(version_object.dataset.project.id, _type, version_object.id)
        object_name = "DatasetVersion with id: " + str(version_object.id)
        return url, object_name

    def get_url_and_id_for_model_version(
        self,
        _type: str,
        version: Union[str, int],
        artifact: Optional[Union[str, int]] = None,
        workspace: Optional[Union[str, int]] = None,
        project: Optional[Union[str, int]] = None,
    ) -> Tuple[str, str]:
        version_object: ModelVersionOutput = ModelVersionApi(self.auth).get_model_version(
            version=version, model=artifact, project=project, workspace=workspace
        )
        model_name = version_object.model.name
        version = version_object.name
        url = self._build_url(version_object.model.project_id, _type, version_object.id)
        object_name = f"Model(name='{model_name}', version='{version}')"
        return url, object_name

    def get_url_for_project(
        self,
        _type: str,
        workspace: Optional[Union[str, int]] = None,
        project: Optional[Union[str, int]] = None,
    ) -> str:
        if project:
            project_object = ProjectApi(self.auth).get_project(project, workspace)
        else:
            raise MissingReferenceError(_type, "attachment")
        return self._build_url(project_object.id, _type, project_object.id)

    @staticmethod
    def _get_version_reference(
        type: str, version: Optional[Union[str, int]] = None, project: Optional[Union[str, int]] = None
    ) -> Union[str, int]:
        if not (isinstance(version, int) or (isinstance(version, str) and project)):
            raise MissingReferenceError(type, PROJECT)
        return version

    @staticmethod
    def _build_url(project_id: int, entity_file_type: str, artifact_id: int) -> str:
        return f"/metadata/project/{project_id}/entityfiles/{entity_file_type}/{artifact_id}"

    def get_attachment(
        self,
        _type: str,
        file_id: int,
        version: Optional[Union[str, int]] = None,
        artifact: Optional[Union[str, int]] = None,
        workspace: Optional[Union[str, int]] = None,
        project: Optional[Union[str, int]] = None,
    ) -> BinaryIO:
        try:
            url, object_id = self._generate_artifact_url_and_id(_type, version, artifact, workspace, project)
            response = self._get_attachment(url + f"/{file_id}")
            self._logger.info(f"Attachment with id: {file_id} successfully retrieved from {object_id}.")
            return cast(BinaryIO, response.raw)
        except HttpError as e:
            self._handle_http_error(e, _type, version, artifact)

    def post_attachment(
        self,
        _type: str,
        version: Optional[Union[str, int]] = None,
        files: Optional[Sequence[Tuple[str, Tuple[Any, BinaryIO]]]] = None,
        artifact: Optional[Union[str, int]] = None,
        workspace: Optional[Union[str, int]] = None,
        project: Optional[Union[str, int]] = None,
        file_id: Optional[int] = None,
    ) -> List[dict]:
        entity_files = []
        try:
            url, object_id = self._generate_artifact_url_and_id(_type, version, artifact, workspace, project)
            if file_id:
                url = url + f"/{file_id}"
                self._logger.info(f"Attachment with id: {file_id} successfully attached to {object_id}.")
            if files and len(files) == 1:
                response = self._post_attachments(url, files)
                if response:
                    entity_files.append(response.json())
                self._logger.info(f"Attachment with name: {files[0][1][0]} successfully attached to {object_id}.")
            elif files and len(files) > 1:
                for file in files:
                    response = self._post_attachments(url, [file])
                    if response:
                        entity_files.append(response.json())
                self._logger.info(
                    f"Attachments with names: {[f[1][0] for f in files]} successfully attached to {object_id}."
                )
            return entity_files
        except HttpError as e:
            if version:
                reference = version
            elif artifact:
                reference = artifact
            elif _type == PROJECT and project:
                reference = project
            else:
                raise ValueError(NO_ARTIFACT_REFERENCE_PROVIDED)
            raise self._httpErrorHandler.handle_get_http_error(e, _type, reference)

    def post_model_attachment(
        self,
        model_type: str,
        model_content: BytesIO,
        version: Optional[Union[str, int]] = None,
        artifact: Optional[Union[str, int]] = None,
        workspace: Optional[Union[str, int]] = None,
        project: Optional[Union[str, int]] = None,
    ) -> None:
        url, object_id = self._generate_artifact_url_and_id("modelversion", version, artifact, workspace, project)
        url += f"?modelFramework={model_type}"
        attachment = ("file", ("model_pickle", model_content))
        self._post_attachments(url, [attachment])
        self._logger.info(f"Model {model_type} successfully attached to {object_id}.")

    def list_attachments(
        self,
        _type: str,
        version: Optional[Union[str, int]] = None,
        artifact: Optional[Union[str, int]] = None,
        workspace: Optional[Union[str, int]] = None,
        project: Optional[Union[str, int]] = None,
    ) -> PagedResponse[AttachmentOutput]:
        url = None
        try:
            url, _ = self._generate_artifact_url_and_id(_type, version, artifact, workspace, project)
        except HttpError as e:
            if version:
                reference = version
            else:
                raise ValueError("No reference to artifact version provided.")
            self._httpErrorHandler.handle_get_http_error(e, _type, reference)
        if url is None:
            raise InvalidReferenceError("artifact version", artifact)
        attachments = self._list_attachments(url)
        return PagedResponse(
            item_cls=AttachmentOutput,
            total=len(attachments),
            page={},
            items=attachments,
        )

    def update_attachments(
        self,
        _type: str,
        files: Sequence[Tuple[str, Tuple[Any, BinaryIO]]],
        version: Optional[Union[str, int]] = None,
        artifact: Optional[Union[str, int]] = None,
        workspace: Optional[Union[str, int]] = None,
        project: Optional[Union[str, int]] = None,
    ):
        try:
            url, object_id = self._generate_artifact_url_and_id(_type, version, artifact, workspace, project)
            attachments = {
                attach.fileName: attach.fileId
                for attach in self.list_attachments(_type, version, artifact, workspace, project).list
            }
            for file in files:
                file_name = file[1][0]
                file_id = attachments.get(file_name)
                if file_id:
                    self._put_attachments(url + f"/{file_id}", [file])
            self._logger.info(
                f"Attachments with names: {[f[1][0] for f in files]} successfully updated in {object_id}."
            )
        except HttpError as e:
            self._handle_http_error(e, _type, version, artifact)

    def _handle_http_error(
        self,
        error: HttpError,
        _type: str,
        version: Optional[Union[str, int]] = None,
        artifact: Optional[Union[str, int]] = None,
    ) -> NoReturn:
        reference = version if version else artifact
        if reference is None:
            raise ValueError(NO_ARTIFACT_REFERENCE_PROVIDED)
        raise self._httpErrorHandler.handle_get_http_error(error, _type, reference)
