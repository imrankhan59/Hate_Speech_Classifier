import os

# Common Constants
ARTIFACT_DIR = "artifacts"
BUCKET_NAME = "GCP_BUCKET_NAME"
ZIP_FILE_NAME = "dataset.zip" # after downoad the zip file, it will be stored in this path
LABEL = "label"  # column name
TWEET = "tweet"  # column name

# Data Ingestion Constants
DATA_INGESTION_ARTIFACTS = "DataIngestionArtifacts"
DATA_INGESTION_IMBALANCE_DATA_DIR = "imbalanced_data.CSV"
DATA_INGESTON_RAW_DATA_DIR = "raw_data.csv"