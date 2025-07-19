import os
import sys
from src.logger import logging
from src.exception import CustomexcEption
from src.components.data_ingestion import DataIngestion
from src.entity.artifact_entity import DataIngestionArtifact
from src.entity.config_entity import DataIngestionConfig


class Training_Pipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

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
            raise CustomexcEption(e, sys) from e
        

    def run_pipeline(self):
        logging.info("Entered the run_pipeline method of Training Pipeline")
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")

            # Further steps like data validation, preprocessing, model training, etc. can be added here

            logging.info("Training Pipeline completed successfully")
        except Exception as e:
            raise CustomexcEption(e, sys) from e
        finally:
            logging.info("Exited run_pipeline method of Training Pipeline")


if __name__ == "__main__":
    pass