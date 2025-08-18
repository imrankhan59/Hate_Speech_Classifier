import os
import sys
import pandas as pd

from zipfile import ZipFile
from src.constant import *
from src.logger import logging
from src.exception import CustomException
from src.configuration.gcloud_syncer import GCloudSyncer
from src.entity.artifact_entity import DataIngestionArtifact
from src.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        os.makedirs(self.data_ingestion_config.DATA_INGESTION_ARTIFACT_DIR, exist_ok=True)
        self.gcloud = GCloudSyncer()

    def get_data_from_gcp(self) -> None:
        try:
            logging.info("Downloading data form GCP bucket")
            self.gcloud.sync_folder_from_gcloud(
                self.data_ingestion_config.BUCKET_NAME,
                self.data_ingestion_config.ZIP_FILE_NAME,
                self.data_ingestion_config.DATA_INGESTION_ARTIFACT_DIR
            )

            logging.info("Data downloaded successfully from GCP bucket")

        except Exception as e:
            raise CustomException(e, sys) from e
    
  
    def load_data(self):
        logging.info("Entering the load_data function of DataIngestion class")
        try:
            raw_data = pd.read_csv(RAW_DATA_PATH)
            imb_data = pd.read_csv(IMB_DATA_PATH)

            raw_data.to_csv(self.data_ingestion_config.RAW_ARTIFACT_DIR, index = False)
            imb_data.to_csv(self.data_ingestion_config.IMBALANCE_ARTIFACT_DIR, index = False)

            return self.data_ingestion_config.IMBALANCE_ARTIFACT_DIR, self.data_ingestion_config.RAW_ARTIFACT_DIR
        except Exception as e:
            raise CustomException(e, sys)
        

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Entered the initiate_data_ingestion method inside DataIngestion class")
        try:
            #self.get_data_from_gcp()
            logging.info("Data Fetched from GCP")


            imbalance_data_path, raw_data_path = self.load_data()
            logging.info("data loaded and path are returned")

            data_ingestion_artifact = DataIngestionArtifact(
                imbalance_data_file_path = imbalance_data_path,
                raw_data_file_path = raw_data_path
            )

            logging.info(f"Data Ingestion artifacts : {data_ingestion_artifact}")

            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys) from e
        

if __name__ == "__main__":
    pass
