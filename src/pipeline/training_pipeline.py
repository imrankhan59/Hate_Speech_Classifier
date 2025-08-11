import os
import sys

from src.logger import logging
from src.exception import CustomException

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig


class Training_Pipeline:
    def __init__(self):
        logging.info("Training Pipeline Started")
        logging.info(60*"*")
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Entered the start_data_ingestion method of Training Pipeline")
        logging.info(60*"_")
        try:
            logging.info("Getting the data from GCP")
            data_ingestion = DataIngestion(data_ingestion_config = self.data_ingestion_config)

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Data ingestion completed successfully")
            logging.info("Exited start_data_ingestion method of Training Pipeline")
            logging.info(60*"_")
            logging.info(60*"*")
            
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        logging.info(60*"_")
        logging.info("Entered the start_data_validation method of Training Pipeline")
        try:
            data_validation = DataValidation(
                data_ingestion_artifact = data_ingestion_artifact,
                data_validation_config = self.data_validation_config
            )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Data validation completed successfully")
            logging.info("Exited start_data_validation method of Training Pipeline")
            logging.info(60*"_")
            logging.info(60*"*")

            return data_validation_artifact
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact,
                                  data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            logging.info(60*"_")
            logging.info("Entered the start_data_transformation method of Training Pipeline")
            data_transformation = DataTransformation(
                data_ingestion_artifact = data_ingestion_artifact,
                data_validation_artifact = data_validation_artifact,
                data_transformation_config = self.data_transformation_config
            )
            data_transformation_artifact = data_transformation.initiate_data_transformation()

            logging.info("Data Transformation completed succesfully")
            logging.info("Exited start_data_transformation method of Training Pipeline")
            logging.info(60*"_")
            logging.info(60*"*")
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) ->ModelTrainerArtifact:
        logging.info(60*"_")
        logging.info("Entered the start_model_trainer method of Training Pipeline")
        try:
            model_trainer = ModelTrainer(
                data_transformation_artifact = data_transformation_artifact,
                model_trainer_config = self.model_trainer_config
            )

            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info("Model Trainer Completed Succesfully")
            logging.info("Exited start_model_trainer method of Training Pipeline")
            logging.info(60*"_")
            logging.info(60*"*")
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e, sys)
               

    def run_pipeline(self):

        logging.info(60*"*")
        logging.info("Entered the run_pipeline method of Training Pipeline")
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")

            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            logging.info(f"Data Validation Artifact: {data_validation_artifact}")
            
            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact = data_ingestion_artifact,
                data_validation_artifact = data_validation_artifact
            )
            logging.info(f"data transfromation Artifact {data_transformation_artifact}")

            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            logging.info(f"Model trainer Artifact")

            logging.info(60*"_")
            logging.info("Training Pipeline completed successfully")
            logging.info(60*"_")
        except Exception as e:
            raise CustomException(e, sys) from e
        finally:
            logging.info("Exited run_pipeline method of Training Pipeline")


if __name__ == "__main__":
    pass