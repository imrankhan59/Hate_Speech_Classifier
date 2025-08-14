import sys
from src.logger import logging
from src.exception import CustomException

from src.configuration.gcloud_syncer import GCloudSyncer
from src.entity.config_entity import ModelPusherConfig
from src.entity.artifact_entity import ModelPusherArtifact


class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig):
        self.model_pusher_config = model_pusher_config
        self.gcloud = GCloudSyncer()

    def initiate_model_pusher(self):
        try:
            logging.info("Entering initiate_model_pusher method of ModelPusher")
            logging.info(f"model bucket_name{self.model_pusher_config.BUCKET_NAME} trained_model_path {self.model_pusher_config.TRAINED_MODEL_PATH}")
            #self.gcloud.sync_folder_to_gcloud(self.model_pusher_config.BUCKET_NAME,
            #                                 self.model_pusher_config.TRAINED_MODEL_PATH,
            #                                  self.model_pusher_config.TRAINED_MODEL_NAME)
            logging.info("uploaded best model to gcloud")

            model_pusher_artifact = ModelPusherArtifact(
                bucket_name = self.model_pusher_config.BUCKET_NAME
            )
            logging.info("Exited the initiate_model_pusher method of ModelPusher Class")
            return model_pusher_artifact

        except Exception as e:
            raise CustomException(e, sys)