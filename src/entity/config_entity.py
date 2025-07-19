import os
from pathlib import Path
from src.constant import *
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    BUCKET_NAME = BUCKET_NAME
    ZIP_FILE_NAME = ZIP_FILE_NAME
    DATA_INGESTION_ARTIFACT_DIR: str = os.path.join(os.getcwd(), ARTIFACT_DIR, DATA_INGESTION_ARTIFACTS)
    IMBALANCE_ARTIFACT_DIR: str = os.path.join(DATA_INGESTION_ARTIFACT_DIR, DATA_INGESTION_IMBALANCE_DATA_DIR)
    RAW_ARTIFACT_DIR: str = os.path.join(DATA_INGESTION_ARTIFACT_DIR, DATA_INGESTON_RAW_DATA_DIR)
    ZIP_FILE_DIR: str = os.path.join(DATA_INGESTION_ARTIFACT_DIR)
    ZIP_FILE_PATH: str = os.path.join(ZIP_FILE_DIR, ZIP_FILE_NAME)
        

