
from enum import Enum


class Framework (str, Enum):
    huggingface = 'HUGGING_FACE'
    sklearn = 'SKLEARN'
    pytorch = 'PYTORCH'
    tensorflow = 'TENSORFLOW'
    xgboost = 'XGBOOST'


class Type (str, Enum):
    tabular = 'TABULAR'
    image = 'IMAGE'
    npl = 'NPL'
    other = 'OTHER'


class Implementation (str, Enum):
    py37 = 'py37'
    py38 = 'py38'
    py39 = 'py39'


class ModelType (str, Enum):
    tabular = 'TABULAR'
    image = 'IMAGE'
    npl = 'NPL'
    other = 'OTHER'


class Server(str, Enum):
    standard_micro = 'STANDARD_MICRO'
    standard_small = 'STANDARD_SMALL'
    standard_medium = 'STANDARD_MEDIUM'
    cpu_optimized_small = 'CPU_OPTIMIZED_SMALL'
    cpu_optimized_medium = 'CPU_OPTIMIZED_MEDIUM'
    cpu_optimized_large = 'CPU_OPTIMIZED_LARGE'
    gpu_optimized_xlarge = 'GPU_OPTIMIZED_XLARGE'
    gpu_optimized_2xlarge = 'GPU_OPTIMIZED_2XLARGE'


class MonitorSchemaType(str, Enum):
    STRING = 'STRING'
    INT = 'INT'
    FLOAT = 'FLOAT'


class MonitorPredictionType(str, Enum):
    CATEGORICAL = 'CATEGORICAL'
    NUMERIC = 'NUMERIC'
