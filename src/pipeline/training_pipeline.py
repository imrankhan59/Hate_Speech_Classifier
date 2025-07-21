import os
import sys

from src.components import data_validation
from src.logger import logging
from src.exception import CustomException

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation

from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig


class Training_Pipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Entered the start_data_ingestion method of Training Pipeline")

        try:
            logging.info("Getting the data from GCP")
            data_ingestion = DataIngestion(data_ingestion_config = self.data_ingestion_config)

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Data ingestion completed successfully")
            logging.info("Exited start_data_ingestion method of Training Pipeline")
            
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        logging.info("Entered the start_data_validation method of Training Pipeline")

        try:
            data_validation = DataValidation(
                data_ingestion_artifact = data_ingestion_artifact,
                data_validation_config = self.data_validation_config
            )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Data validation completed successfully")
            logging.info("Exited start_data_validation method of Training Pipeline")

            return data_validation_artifact
        except Exception as e:
            raise CustomException(e, sys) from e
        

    def run_pipeline(self):
        logging.info("Entered the run_pipeline method of Training Pipeline")
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            logging.info(f"Data Validation Artifact: {data_validation_artifact}")
            # Further steps like data validation, preprocessing, model training, etc. can be added here

            logging.info("Training Pipeline completed successfully")
        except Exception as e:
            raise CustomException(e, sys) from e
        finally:
            logging.info("Exited run_pipeline method of Training Pipeline")


if __name__ == "__main__":
    pass