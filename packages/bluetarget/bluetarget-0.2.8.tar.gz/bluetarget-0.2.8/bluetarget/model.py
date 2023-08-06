

from typing import Dict, List

from bluetarget.api_endpoint import APIEndpoint
from bluetarget.errors import AuthorizationError, EntityNotFound, ServerValidationException
from bluetarget.model_version import ModelVersion


class Model:
    api_key: str
    model_id: str
    endpoint: APIEndpoint
    data: Dict

    def __init__(self, api_key: str, model_id: str = None) -> None:
        self.api_key = api_key
        self.endpoint = APIEndpoint(api_key)
        self.model_id = model_id

    def set_model_id(self, id):
        self.model_id = id

    def get(self, model_id: str):
        response, status = self.endpoint.get(f"models/{model_id}")

        if status == 403:
            raise AuthorizationError()

        if status == 404:
            raise EntityNotFound("Model", model_id)

        if status != 200:
            raise ServerValidationException(
                response['code'], response['description'])

        self.data = response
        self.set_model_id(response['id'])

        return response

    def create(self, name: str, **kwargs):

        body = {
            "name": name
        }

        for key in kwargs:
            body[key] = kwargs[key]

        response, status = self.endpoint.post("models/", body=body)

        if status == 403:
            raise AuthorizationError()

        if status != 200:
            raise ServerValidationException(
                response['code'], response['description'])

        self.data = response
        self.set_model_id(response['id'])

        return response

    def create_version(self, model_class: str, model_files: List[str], requirements_file: str, **kwargs) -> ModelVersion:
        model_version = ModelVersion(
            api_key=self.api_key, model_id=self.data["id"])

        model_version.create(
            model_class=model_class,
            model_files=model_files,
            requirements_file=requirements_file,
            **kwargs
        )

        return model_version

    def get_version(self, model_version_id: str):
        model_version = ModelVersion(
            api_key=self.api_key, model_id=self.model_id)

        model_version.get(model_version_id=model_version_id)

        return model_version

    def health(self):
        return self.endpoint.get(
            f"models/{self.model_id}/health")

    def predict(self, inputs: List):
        body = {
            "inputs": inputs
        }
        return self.endpoint.post(
            f"models/{self.model_id}/predict", body)
