import pandas
from typing import List, Optional

from bluetarget.entities import Prediction, PredictionActual, ColumnMapping, ModelSchema, ModelSchemaVersion

from bluetarget.api_endpoint import APIEndpoint
from bluetarget.errors import AuthorizationError, ServerValidationException

from io import BytesIO

from datetime import datetime, timedelta, timezone

import requests


class Monitor:
    api_key: str
    endpoint: APIEndpoint
    monitor_id: str
    version_id: str

    def __init__(self, api_key: str, monitor_id: str = None, version_id: str = None) -> None:
        self.api_key = api_key
        self.monitor_id = monitor_id
        self.version_id = version_id

        self.endpoint = APIEndpoint(api_key)

    def create(self, model_schema: ModelSchema):

        body = model_schema.dict()

        response, status = self.endpoint.post("monitor/", body=body)

        if status == 403:
            raise AuthorizationError()

        if status != 200:
            raise ServerValidationException(status, response['code'])

        self.monitor_id = response["id"]

        return response

    def create_version(self, model_schema_id: str, model_schema_version: ModelSchemaVersion):
        body = model_schema_version.dict()

        if "model_schema" in body:
            body["schema"] = body.pop("model_schema")

        response, status = self.endpoint.post(
            f"monitor/{model_schema_id}/versions", body=body)

        if status == 403:
            raise AuthorizationError()

        if status != 200:
            raise ServerValidationException(status, response['code'])

        self.version_id = response["id"]

        return response

    def get_inference_dataset(self, start_time: Optional[datetime] = None,
                              end_time: Optional[datetime] = None,
                              actual_value_required: bool = False) -> pandas.DataFrame:
        if not end_time:
            end_time = datetime.now(tz=timezone.utc)
        if not start_time:
            start_time = end_time - timedelta(days=7)

        query = {
            "started_at": start_time.isoformat(),
            "ended_at": end_time.isoformat(),
            "actual_value_required": actual_value_required
        }

        response, status = self.endpoint.get(
            f"monitor/{self.monitor_id}/versions/{self.version_id}/download-data", query=query)

        if status == 403:
            raise AuthorizationError()

        if status != 200:
            raise ServerValidationException(status, response['code'])

        url = response["url"]

        response = requests.get(url)

        buffer = BytesIO(response.content)

        return pandas.read_parquet(buffer)

    def add_reference_dataset(self, dataset: pandas.DataFrame, column_mapping: ColumnMapping):

        body = column_mapping.dict()

        response, status = self.endpoint.post(
            f"monitor/{self.monitor_id}/versions/{self.version_id}/upload-reference", body=body)

        if status == 403:
            raise AuthorizationError()

        if status != 200:
            raise ServerValidationException(status, response['code'])

        url = response["uploadUrl"]
        fields = response["formData"]

        buffer = BytesIO()
        dataset.to_parquet(buffer, engine="pyarrow")

        buffer.seek(0)

        files = {'file': ('file.parquet', buffer)}
        response = requests.post(url, data=fields, files=files)

    def log_predictions(self, predictions: List[Prediction]):

        data = []

        for prediction in predictions:
            data.append(prediction.dict())

        body = {
            "data": data,
        }

        response, status = self.endpoint.post(
            f"monitor/{self.monitor_id}/versions/{self.version_id}/predictions", body=body)

        if status == 403:
            raise AuthorizationError()

        if status != 200:
            raise ServerValidationException(status, response['code'])

        return response

    def log_actuals(self, actuals: List[PredictionActual]):

        data = []

        for actual in actuals:
            data.append(actual.dict())

        body = {
            "data": data,
        }

        response, status = self.endpoint.post(
            f"monitor/{self.monitor_id}/versions/{self.version_id}/actuals", body=body)

        if status == 403:
            raise AuthorizationError()

        if status != 200:
            raise ServerValidationException(status, response['code'])

        return response
