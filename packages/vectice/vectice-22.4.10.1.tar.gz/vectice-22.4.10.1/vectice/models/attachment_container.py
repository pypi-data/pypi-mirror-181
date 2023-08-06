import logging
import os
from typing import BinaryIO, Union, List

import io

from vectice.api import Client
from vectice.api.json.attachment import AttachmentOutput

_logger = logging.getLogger(__name__)

FILE_PATH_DOES_NOT_EXIST_ERROR_MESSAGE = "The file path '%s' is not valid. The file does not exist."


class AttachmentContainer:
    def __init__(self, name: str, id: int, client: Client, container_type: str):
        self._client = client
        self._id = id
        self._name = name
        self._container_type = container_type

    def list_attachments(self) -> List[str]:
        """
        List attachments of the entity

        """
        return [attachment.fileName for attachment in self.attachments]

    def add_attachments(self, file_paths: Union[str, List[str]]):
        """
        Add a single or a set of attachments to the entity.

        :param file_paths: the paths of the attachment
        """
        attached_files = self.list_attachments()
        file_paths = [file_paths] if isinstance(file_paths, str) else file_paths
        attachments = self._add_files_to_attachments(file_paths, attached_files)
        return self._client.create_attachments(self._container_type.lower(), attachments, self._id)

    def _add_files_to_attachments(self, file_paths: List[str], attached_files: List[str]):
        attachments = []
        for file_path in file_paths:
            if not os.path.exists(file_path):
                raise ValueError(FILE_PATH_DOES_NOT_EXIST_ERROR_MESSAGE % file_path)
            curr_file = ("file", (file_path, open(file_path, "rb")))
            attachments.append(curr_file)
            file_name = file_path.split("/")[-1]
            if file_name in attached_files:
                raise RuntimeError(f"'{file_paths}' is already attached to '{self._name}'")
        return attachments

    def get_attachment(self, file_path: str) -> BinaryIO:
        """
        Get an attachment content from the entity

        :param file_path: the path to the attachment

        :return: BinaryIO
        """
        try:
            attachment_list = {
                attach.fileName: attach.fileId
                for attach in self._client.list_attachments(self._container_type.lower(), self._id).list
            }
        except Exception as e:
            raise ValueError(f"list of attachment for {self._container_type} failed . Due to {e}")
        file_id = attachment_list.get(file_path)
        if file_id:
            try:
                return self._client.get_attachment(self._container_type.lower(), file_id, self._id)
            except Exception as e:
                raise ValueError(
                    f"{self._container_type} attachment failed to retrieve attachment named '{file_path}' due to:\n {e}"
                )
        else:
            raise ValueError(
                f"{self._container_type} attachment failed to retrieve attachment named '{file_path}'. Please check the filename."
            )

    def get_attachment_as_file(self, file_path: str, saved_path: str):
        """
        Get an attachment content from the entity and store it in a file

        :param file_path: the path to the file
        :param saved_path: the path to the file

        :return: None
        """
        attachment = self.get_attachment(file_path)
        with open(saved_path, "wb") as content:
            while True:
                chunk = attachment.read(128)
                if not chunk:
                    break
                content.write(chunk)

    @property
    def attachments(self) -> List[AttachmentOutput]:
        """
        List attachments of the entity

        """
        return self._client.list_attachments(self._container_type.lower(), self._id).list

    def add_serialized_model(self, model_type: str, model_content: bytes):
        self._client.create_model_attachment(model_type, io.BytesIO(model_content), self._id)
