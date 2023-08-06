from bluetarget.bluetarget_types import MonitorSchemaType, MonitorPredictionType
from pydantic import BaseModel, Field, constr, validator
from typing import Dict, Union, List, Optional
from datetime import datetime

EntityValue = Union[str, int, float]


class ModelSchema(BaseModel):
    name: str
    monitorId: Optional[str] = None
    description: Optional[str] = None
    predictionType: MonitorPredictionType


class ModelSchemaVersion(BaseModel):
    versionId: Optional[str] = None
    model_schema: Dict[str, MonitorSchemaType]


class Prediction(BaseModel):
    prediction_id: constr(min_length=1, max_length=64)
    features: Dict[str, EntityValue]
    value: EntityValue
    probabilities: Optional[Dict[str, float]] = Field(default_factory=dict)
    shap_values: Optional[Dict[str, float]] = Field(default_factory=dict)
    created_at: Optional[datetime]

    @validator("created_at")
    def serialize_created_at(cls, value):
        if value is None:
            return None

        return value.strftime('%Y-%m-%d %H:%M:%S')

    class Config:
        smart_union = True


class PredictionActual(BaseModel):
    prediction_id: constr(min_length=1, max_length=64)
    value: EntityValue
    created_at: Optional[datetime]

    @validator("created_at")
    def serialize_created_at(cls, value):
        if value is None:
            return None

        return value.strftime('%Y-%m-%d %H:%M:%S')

    class Config:
        smart_union = True


class ColumnMapping(BaseModel):
    features: List[str]
    target: Optional[str] = None
    prediction: Optional[str] = None
    datatime: Optional[str] = None

    class Config:
        smart_union = True
