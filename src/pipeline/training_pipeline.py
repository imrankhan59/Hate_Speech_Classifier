import os
import sys

from src.components import model_pusher
from src.logger import logging
from src.exception import CustomException

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher

from src.entity.artifact_entity import (DataIngestionArtifact,
                                        DataValidationArtifact, 
                                        DataTransformationArtifact,
                                        ModelPusherArtifact, 
                                        ModelTrainerArtifact, 
                                        ModelEvaluationArtifact)
from src.entity.config_entity import (DataIngestionConfig,
                                        DataValidationConfig, 
                                        DataTransformationConfig, 
                                        ModelTrainerConfig, 
                                        ModelEvaluationConfig,
                                        ModelPusherConfig)


class Training_Pipeline:
    def __init__(self):
        logging.info("Training Pipeline Started")
        logging.info(60*"*")
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
        self.model_pusher_config = ModelPusherConfig()

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
    
    def start_model_evaluation(self, model_trainer_artifact: ModelTrainerArtifact, data_transoformation_artifact: DataTransformationArtifact):
        logging.info(60*"_")
        logging.info("Entered the start_model_evaluation method of Training Pipeline")
        try:
            model_evaluation = ModelEvaluation(model_evaluation_config=self.model_evaluation_config, model_trainer_artifacts=model_trainer_artifact, data_transformation_artifact=data_transoformation_artifact)
            model_trainer_artifact = model_evaluation.initiate_model_evaluation()
            
            logging.info("Model Evaluation Completed Succesfully")
            logging.info("Exited start_model_evaluation method of Training Pipeline")
            logging.info(60*"_")
            logging.info(60*"*")
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e, sys)
        
    def start_model_pusher(self):
        logging.info(60*"_")
        logging.info("Entered the start_model_pusher method of Training Pipeline")

        try:
            model_pusher = ModelPusher(model_pusher_config = self.model_pusher_config)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            logging.info("Model pusher Completed Succesfully")
            logging.info("Exited start_model_pusher method of Training Pipeline")
            logging.info(60*"_")
            logging.info(60*"*")

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

            model_evaluation_artifact = self.start_model_evaluation(model_trainer_artifact = model_trainer_artifact, data_transoformation_artifact = data_ingestion_artifact)
            logging.info(f"Model Evaluation Artifact {model_evaluation_artifact}")

            model_pusher_artifact = self.start_model_pusher()
            logging.info(f"Model Pusher Artifacts {model_pusher_artifact}")
            logging.info(60*"_")
            logging.info("Training Pipeline completed successfully")
            logging.info(60*"_")
        except Exception as e:
            raise CustomException(e, sys) from e
        finally:
            logging.info("Exited run_pipeline method of Training Pipeline")


if __name__ == "__main__":
    pass