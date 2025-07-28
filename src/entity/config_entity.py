import os
from pathlib import Path
from sre_constants import IN
from src.constant import *
from dataclasses import dataclass, field

@dataclass
class DataIngestionConfig:
    BUCKET_NAME = BUCKET_NAME
    ZIP_FILE_NAME = ZIP_FILE_NAME
    DATA_INGESTION_ARTIFACT_DIR: str = os.path.join(os.getcwd(), ARTIFACT_DIR, DATA_INGESTION_ARTIFACTS)
    IMBALANCE_ARTIFACT_DIR: str = os.path.join(DATA_INGESTION_ARTIFACT_DIR, DATA_INGESTION_IMBALANCE_DATA_DIR)
    RAW_ARTIFACT_DIR: str = os.path.join(DATA_INGESTION_ARTIFACT_DIR, DATA_INGESTON_RAW_DATA_DIR)
    ZIP_FILE_DIR: str = os.path.join(DATA_INGESTION_ARTIFACT_DIR)
    ZIP_FILE_PATH: str = os.path.join(ZIP_FILE_DIR, ZIP_FILE_NAME)


@dataclass
class DataValidationConfig:
    DATA_VALIDATION_ARTIFACT_DIR: str = os.path.join(os.getcwd(), ARTIFACT_DIR, DATA_VALIDATION_ARTIFACTS)
    DATA_VALIDATION_REPORT_FILE_PATH: str = os.path.join(DATA_VALIDATION_ARTIFACT_DIR, DATA_VALIDATION_REPORT_FILE_NAME)
    DATA_VALIDATION_SCHEMA_FILE_NAME: str = DATA_VALIDATION_SCHEMA_FILE_NAME
        
@dataclass
class DataTransformationConfig:
    DATA_TRANSFORMATION_ARTIFACT_DIR: str = os.path.join(os.getcwd(), ARTIFACT_DIR, DATA_TRANSFORMATION_ARTIFACTS)
    TRANSFORMED_FILE_PATH: str = os.path.join(DATA_TRANSFORMATION_ARTIFACT_DIR, TRANSFORMED_FILE_NAME)
    ID: str = ID
    AXIS: int = AXIS
    DROP_COLUMN: list = DROP_COLUMN
    DROP_COLUMN: list = field(default_factory=lambda: DROP_COLUMN)
    INPLACE: bool = INPLACE
    CLASS: str = CLASS
    LABEL: str = LABEL
    TWEET: str = TWEET
