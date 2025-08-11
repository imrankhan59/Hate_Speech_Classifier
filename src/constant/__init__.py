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
DATA_INGESTON_RAW_DATA_DIR = "raw_data4.csv"


# Data Validation Constants
DATA_VALIDATION_ARTIFACTS = "DataValidationArtifacts"
DATA_VALIDATION_REPORT_FILE_NAME = "data_validation_report.yaml"
DATA_VALIDATION_SCHEMA_FILE_NAME = "schema.yaml"

# Data Transformation Constants
DATA_TRANSFORMATION_ARTIFACTS = "DataTransformationArtifacts"
TRANSFORMED_FILE_NAME = "transformed_data.csv"
DATA_DIR = "data"
ID = "id"
AXIS = 1
INPLACE = True
DROP_COLUMN = ['count', 'hate_speech', 'offensive_language', 'neither']
CLASS = "class"

# Model Trainer

MODEL_TRAINER_ARTIFACTS = "ModelTrainerArtifacts"
TRAINED_MODEL_DIR = "trained_model"
TRAINED_MODEL_NAME = "model.h5"
X_TEST_FILE_NAME = "x_test.csv"
Y_TEST_FILE_NAME = "y_test.csv"

X_TRAIN_FILE_NAME = "x_train.csv"

RANDOM_STATE = 42
EPOCH = 1
BATCH_SIZE = 128
VALIDATION_SPLIT = 0.2

MAX_WORD = 50000
MAX_LEN = 300
LOSS = "binary_crossentrophy"
METRICS = ["accuracy"]
ACTIVATION = "sigmoid"