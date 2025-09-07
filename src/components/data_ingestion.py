import os
import sys
import pandas as pd

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

    def load_data(self):
        logging.info("Entering the load_data function of DataIngestion class")
        try:
            #  Step 1: if data already exists (from DVC pull), skip ingestion
            if os.path.exists(self.data_ingestion_config.RAW_ARTIFACT_DIR) and \
            os.path.exists(self.data_ingestion_config.IMBALANCE_ARTIFACT_DIR):
                logging.info("Raw and imbalance data already exist (probably from DVC pull). Skipping ingestion.")
                return (
                    self.data_ingestion_config.IMBALANCE_ARTIFACT_DIR,
                    self.data_ingestion_config.RAW_ARTIFACT_DIR
                )

            #  Step 2: else, try to fetch from your local paths
            logging.info("Artifact files not found, reading from local source paths...")
            
            if not os.path.exists(RAW_DATA_PATH) or not os.path.exists(IMB_DATA_PATH):
                raise FileNotFoundError(
                    f"Source data not found. RAW_DATA_PATH={RAW_DATA_PATH}, IMB_DATA_PATH={IMB_DATA_PATH}"
                )

            raw_data = pd.read_csv(RAW_DATA_PATH)
            imb_data = pd.read_csv(IMB_DATA_PATH)

            # Save artifacts
            raw_data.to_csv(self.data_ingestion_config.RAW_ARTIFACT_DIR, index=False)
            imb_data.to_csv(self.data_ingestion_config.IMBALANCE_ARTIFACT_DIR, index=False)

            return (
                self.data_ingestion_config.IMBALANCE_ARTIFACT_DIR,
                self.data_ingestion_config.RAW_ARTIFACT_DIR
            )
        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Entered the initiate_data_ingestion method inside DataIngestion class")
        try:
            imbalance_data_path, raw_data_path = self.load_data()
            logging.info("Data loaded and paths are returned")

            data_ingestion_artifact = DataIngestionArtifact(
                imbalance_data_file_path=imbalance_data_path,
                raw_data_file_path=raw_data_path
            )

            logging.info(f"Data Ingestion artifacts : {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys) from e


if __name__ == "__main__":
    data_ingest_config = DataIngestionConfig()
    obj = DataIngestion(data_ingestion_config=data_ingest_config)
    obj.initiate_data_ingestion()

